import os
import django
from django.db.models import Sum, Q, F

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horizon_analytics.settings')
django.setup()

from analytics_projects.models import Project, Funding, Location

# ------------------------------
# Funzione base per filtrare progetti
# ------------------------------
def get_filtered_projects(filters):
    """Restituisce i progetti filtrati per regione e macroarea, con total_financing annotato."""
    region = filters.get("region")
    macroarea = filters.get("macroarea")

    projects_qs = Project.objects.prefetch_related("locations").annotate(
        total_financing=Sum("funding__total_funds_gross")
    )

    if region and region != "nessun filtro":
        projects_qs = projects_qs.filter(locations__region_code=region)

    if macroarea and macroarea != "nessun filtro":
        projects_qs = projects_qs.filter(locations__macroarea=macroarea)

    return projects_qs.distinct()


# ------------------------------
# Top 10 progetti per finanziamento
# ------------------------------
def top_10_projects(filters):
    projects_qs = get_filtered_projects(filters)

    top_projects_qs = projects_qs.order_by("-total_financing")[:10]

    result = {}
    for index, project in enumerate(top_projects_qs, start=1):
        regions_str = ", ".join([loc.region_name for loc in project.locations.all()])
        macroareas_str = ", ".join([loc.macroarea for loc in project.locations.all()])

        result[f"project{index}"] = {
            "id": project.local_project_code,
            "title": project.oc_project_title,
            "total_financing": project.total_financing or 0,
            "region": regions_str,
            "macroarea": macroareas_str,
        }

    return result


# ------------------------------
# Top 3 settori per finanziamento
# ------------------------------
def get_top_sectors(filters):
    projects_qs = get_filtered_projects(filters)

    fundings = Funding.objects.filter(project__in=projects_qs).values(
        "project__cup_descr_sector"
    ).annotate(
        total=Sum("total_funds_gross")
    ).order_by("-total")[:3]

    result = {}
    for i, x in enumerate(fundings, start=1):
        result[f"sector{i}"] = {
            "name": x["project__cup_descr_sector"],
            "total_financing": x["total"] or 0
        }

    return result


#
#  ------------------------------
# Numero di progetti grandi (>50M)
# ------------------------------
def count_big_projects(filters):
    projects_qs = get_filtered_projects(filters)
    big_project_threshold = 50_000_000

    return projects_qs.filter(funding__total_funds_gross__gte=big_project_threshold).distinct().count()


# ------------------------------
# Finanziamenti per macroarea
# ------------------------------
def funding_by_macroarea(filters):
    projects_qs = Project.objects.all() #no filter because we want see only middle north and midday
    fundings = Funding.objects.filter(project__in=projects_qs).distinct()

    result = fundings.values("project__locations__macroarea").annotate(
        total=Sum("total_funds_gross")
    )

    return {
        item["project__locations__macroarea"]: item["total"] or 0
        for item in result
    }

# ------------------------------
# Conteggio progetti per stato
# ------------------------------
def count_projects_with_status(filters):
    projects_qs = get_filtered_projects(filters)

    not_started_projects = projects_qs.filter(
        oc_project_status=Project.ProjectStatusChoices.NOT_STARTED
    ).distinct()

    in_progress_projects = projects_qs.filter(
        oc_project_status=Project.ProjectStatusChoices.ONGOING
    ).distinct()

    concluded_projects = projects_qs.filter(
        oc_project_status=Project.ProjectStatusChoices.CONCLUDED
    ).distinct()

    liquidated_projects = projects_qs.filter(
        oc_project_status=Project.ProjectStatusChoices.LIQUIDATED
    ).distinct()

    return {
        "total": projects_qs.count(),
        "not_started": not_started_projects.count(),
        "in_progress": in_progress_projects.count(),
        "concluded": concluded_projects.count(),
        "liquidated": liquidated_projects.count()
    }


# ------------------------------
# Somma totale dei finanziamenti
# ------------------------------
def sum_funding_gross(filters):
    projects_qs = get_filtered_projects(filters)
    fundings = Funding.objects.filter(project__in=projects_qs).distinct()

    result = fundings.aggregate(total_gross=Sum('total_funds_gross'))
    return result['total_gross'] or 0


# ------------------------------
# Restituisce un queryset di Funding filtrato secondo i filtri del contratto:
#     - macroarea: Centro-Nord, Mezzogiorno, etc.
#     - funding_source: UE, Stato, Regioni, Privato, Comune, Provincia, Altro_Pubblico
#     Non filtra progetti a caso, serve solo a limitare i fundings considerati per le aggregazioni.
# ------------------------------
def apply_filters(filters):
    macroarea = filters.get("macroarea")
    funding_source = filters.get("funding_source")

    # Partiamo da tutti i progetti
    projects_qs = Project.objects.all()

    # Filtro per macroarea (solo se specificato)
    if macroarea and macroarea != "Tutte":
        projects_qs = projects_qs.filter(locations__macroarea=macroarea)

    # Tutti i fundings relativi ai progetti filtrati
    funding_qs = Funding.objects.filter(project__in=projects_qs)

    # Filtro per funding_source (solo se specificato e diverso da "Tutte")
    if funding_source and funding_source != "Tutte":
        if funding_source == "UE":
            funding_qs = funding_qs.filter(
                Q(eu_funds__gt=0) |
                Q(eu_funds_fesr__gt=0) |
                Q(eu_funds_fse__gt=0) |
                Q(eu_funds_feasr__gt=0) |
                Q(eu_funds_feamp__gt=0) |
                Q(eu_funds_iog__gt=0)
            )
        elif funding_source == "Stato":
            funding_qs = funding_qs.filter(
                Q(state_rotating_fund__gt=0) |
                Q(state_fsc__gt=0) |
                Q(state_pac__gt=0) |
                Q(state_completions__gt=0) |
                Q(state_other_measures__gt=0)
            )
        elif funding_source == "Regioni":
            funding_qs = funding_qs.filter(regional_funds__gt=0)
        elif funding_source == "Privato":
            funding_qs = funding_qs.filter(private_funds__gt=0)
        elif funding_source == "Comune":
            funding_qs = funding_qs.filter(municipal_funds__gt=0)
        elif funding_source == "Provincia":
            funding_qs = funding_qs.filter(provincial_funds__gt=0)
        elif funding_source == "Altro_Pubblico":
            funding_qs = funding_qs.filter(other_public_funds__gt=0)

    return funding_qs


# ------------------------------
# Somma totale delle fonti di finanziamento
# ------------------------------
def funding_sources_analysis(filters):
    projects, funding = apply_filters(filters)

    data = funding.aggregate(
        UE=Sum("eu_funds"),
        Stato=Sum(
            F("state_rotating_fund") +
            F("state_fsc") +
            F("state_pac") +
            F("state_completions") +
            F("state_other_measures")
        ),
        Regioni=Sum("regional_funds"),
        Privato=Sum("private_funds"),
        Comune=Sum("municipal_funds"),
        Altro_Pubblico=Sum("other_public_funds"),
        Provincia=Sum("provincial_funds"),
    )

    return {k: float(v or 0) for k, v in data.items()}
