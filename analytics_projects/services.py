import os
import django
from django.db.models import Sum, Q, F

from django.db.models import Prefetch
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horizon_analytics.settings')

# Initialize Django
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

def get_filtered_projects_analysis(filters):
    """
    filter by funding_source and macroarea
    """
    funding_source = filters.get("funding_source")
    macroarea = filters.get("macroarea")

    projects_qs = Project.objects.all()

    # Filtro per macroarea
    if macroarea and macroarea != "Tutte":
        projects_qs = projects_qs.filter(locations__macroarea=macroarea)

    # Prefetch dei funding in base al funding_source
    if funding_source and funding_source != "Tutte":
        # Definiamo il filtro dinamico sul funding
        # assumiamo che funding_source sia lo stesso nome del campo in Funding
        funding_prefetch = Prefetch(
            "funding",
            queryset=Funding.objects.only(
                funding_source,  # il campo specifico richiesto
                "total_funds_gross",
                "total_funds_net",
                "total_savings",
                "total_public_savings"
            ),
            to_attr="filtered_funding"
        )
        projects_qs = projects_qs.prefetch_related(funding_prefetch)
    else:
        # Tutti i funding
        projects_qs = projects_qs.prefetch_related("funding")

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
    projects_qs = Project.objects.prefetch_related("funding", "locations")

    macroarea = filters.get("macroarea")
    funding_source = filters.get("funding_source")

    if macroarea and macroarea != "Tutte":
        projects_qs = projects_qs.filter(locations__macroarea=macroarea)

    # Filtraggio per funding_source se necessario
    funding_qs = Funding.objects.filter(project__in=projects_qs)

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

    return projects_qs.distinct(), funding_qs.distinct()




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


# ------------------------------
# Somma totale delle fonti di finanziamento SPECIFICHE
# ------------------------------
def specific_funds_contribution(filters):
    projects, funding = apply_filters(filters)

    data = funding.aggregate(
        fesr=Sum("eu_funds_fesr"),
        fse=Sum("eu_funds_fse"),
        feasr=Sum("eu_funds_feasr"),
        feamp=Sum("eu_funds_feamp"),
        iog=Sum("eu_funds_iog"),
        fsc=Sum("state_fsc"),
        rot=Sum("state_rotating_fund"),
        pac=Sum("state_pac"),
        comp=Sum("state_completions"),
        altri_stato=Sum("state_other_measures"),
    )

    return {
        "FESR_UE": float(data["fesr"] or 0),
        "FSE_UE": float(data["fse"] or 0),
        "FSC_Stato": float(data["fsc"] or 0),
        "Fondo_di_Rotazione_Stato": float(data["rot"] or 0),
        "FEASR_UE": float(data["feasr"] or 0),
        "FEAMP_UE": float(data["feamp"] or 0),
        "IOG_UE": float(data["iog"] or 0),
        "PAC_Stato": float(data["pac"] or 0),
        "Completamenti_Stato": float(data["comp"] or 0),
        "Altri_Stato": float(data["altri_stato"] or 0),
    }


# ------------------------------
# Top 10 tematiche con il maggior valore di finanziamento
# ------------------------------
def top10_thematic_objectives(filters):
    projects, funding = apply_filters(filters)

    themes = (
        projects.values("oc_synthetic_theme")
        .annotate(amount=Sum("funding__total_funds_gross"))
        .order_by("-amount")[:10]
    )

    return [
        {
            "description": t["oc_synthetic_theme"] or "Non specificato",
            "amount": float(t["amount"] or 0)
        }
        for t in themes
    ]

def get_funds_to_be_found(filters):
    """
    Ritorna:
    - numero progetti con savings > 0
    - totale saving
    """
    projects = get_filtered_projects_analysis(filters)
    # Prefetch funding per evitare N+1 queries
    projects = projects.prefetch_related("funding")

    number_of_projects_with_gap = 0
    total_missing_amount = 0

    for p in projects:
        total_savings = sum((f.total_savings or 0) for f in p.funding.all())

        if total_savings > 0:
            number_of_projects_with_gap += 1
            total_missing_amount += total_savings

    return {
        "number_of_projects_with_gap": number_of_projects_with_gap,
        "total_missing_amount": total_missing_amount
    }

def get_payments_realization_gap(filters):
    """
    give a dictionary with total realized cost, total payment and difference between them
    """
    # no filters
    projects = Project.objects.all()

    # Aggrega i valori dei finanziamenti dei progetti filtrati
    aggregation = Funding.objects.filter(project__in=projects).aggregate(
        total_realized_cost=Sum('total_funds_gross'),
        total_payments_made=Sum('total_funds_net'),
    )

    total_realized_cost = aggregation['total_realized_cost'] or 0
    total_payments_made = aggregation['total_payments_made'] or 0
    overall_difference = total_realized_cost - total_payments_made

    return {
        "total_realized_cost": total_realized_cost,
        "total_payments_made": total_payments_made,
        "overall_difference": overall_difference
    }

def get_top_project_typologies():
    projects_qs = get_filtered_projects(filters={})

    fundings = (
        Funding.objects
        .filter(
            project__in=projects_qs,
            project__cup_typology__isnull=False
        )
        .values("project__cup_typology")
        .annotate(total=Sum("total_funds_gross"))
        .order_by("-total")[:10]
    )

    result = []
    for x in fundings:
        result.append({
            "type": x["project__cup_typology"] or "sconosciuto",
            "amount": x["total"] or 0
        })

    return result
