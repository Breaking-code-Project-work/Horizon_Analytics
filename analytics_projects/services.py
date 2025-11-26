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
    """Restituisce i progetti filtrati per regione, macroarea e is_trasversale, con total_financing annotato."""
    region = filters.get("region")
    macroarea = filters.get("macroarea")
    is_trasversale = filters.get("is_trasversale")

    projects_qs = Project.objects.prefetch_related("locations").annotate(
        total_financing=Sum("funding__total_funds_gross")
    )

    if region and region != "nessun filtro":
        projects_qs = projects_qs.filter(locations__region_code=region)

    if macroarea and macroarea != "nessun filtro":
        projects_qs = projects_qs.filter(locations__macroarea=macroarea)

    if is_trasversale is not None:
        if str(is_trasversale).lower() == "true":
            projects_qs = projects_qs.filter(is_trasversale=True)
        elif str(is_trasversale).lower() == "false":
            projects_qs = projects_qs.filter(is_trasversale=False)

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
# Funzione base per filtrare progetti per macroarea
# ------------------------------
def get_filtered_projects_by_filters(filters):
    """
    Restituisce:
      - projects_qs filtrati per macroarea
      - funding_qs filtrato per funding_source
    """
    macroarea = filters.get("macroarea")
    funding_source = filters.get("funding_source")

    # --------------------------
    # Filtra i progetti per macroarea
    # --------------------------
    projects_qs = Project.objects.prefetch_related("locations").distinct()
    if macroarea and macroarea != "Tutte":
        projects_qs = projects_qs.filter(locations__macroarea=macroarea)

    # --------------------------
    # Filtra i finanziamenti per funding_source
    # --------------------------
    funding_qs = Funding.objects.filter(project__in=projects_qs)
    if funding_source and funding_source != "Tutte":
        source_map = {
            "UE": Q(eu_funds__gt=0) | Q(eu_funds_fesr__gt=0) | Q(eu_funds_fse__gt=0) |
                  Q(eu_funds_feasr__gt=0) | Q(eu_funds_feamp__gt=0) | Q(eu_funds_iog__gt=0),
            "Stato": Q(state_rotating_fund__gt=0) | Q(state_fsc__gt=0) | Q(state_pac__gt=0) |
                     Q(state_completions__gt=0) | Q(state_other_measures__gt=0),
            "Regioni": Q(regional_funds__gt=0),
            "Privato": Q(private_funds__gt=0),
            "Comune": Q(municipal_funds__gt=0),
            "Provincia": Q(provincial_funds__gt=0),
            "Altro_Pubblico": Q(other_public_funds__gt=0),
        }
        if funding_source in source_map:
            funding_qs = funding_qs.filter(source_map[funding_source])

    return projects_qs.distinct(), funding_qs.distinct()


# ------------------------------
# Somma totale delle fonti di finanziamento
# ------------------------------
def funding_sources_analysis(filters):
    projects_qs, funding_qs = get_filtered_projects_by_filters(filters)
    funding_source = filters.get("funding_source")

    all_sources = ["UE", "Stato", "Regioni", "Privato", "Comune", "Provincia", "Altro_Pubblico"]

    source_fields = {
        "UE": ["eu_funds"],
        "Stato": ["state_rotating_fund", "state_fsc", "state_pac", "state_completions", "state_other_measures"],
        "Regioni": ["regional_funds"],
        "Privato": ["private_funds"],
        "Comune": ["municipal_funds"],
        "Provincia": ["provincial_funds"],
        "Altro_Pubblico": ["other_public_funds"]
    }

    output_map = {
        "eu_funds": "UE",
        "state_fsc": "Stato",
        "state_rotating_fund": "Stato",
        "state_pac": "Stato",
        "state_completions": "Stato",
        "state_other_measures": "Stato",
        "regional_funds": "Regioni",
        "private_funds": "Privato",
        "municipal_funds": "Comune",
        "provincial_funds": "Provincia",
        "other_public_funds": "Altro_Pubblico"
    }

    if funding_source in source_fields:
        fields_to_aggregate = source_fields[funding_source]
    else:
        fields_to_aggregate = sum(source_fields.values(), [])

    agg = funding_qs.aggregate(**{f: Sum(f) for f in fields_to_aggregate})

    result = {s: 0.0 for s in all_sources}
    for f in fields_to_aggregate:
        key = output_map[f]
        result[key] += float(agg.get(f, 0) or 0)

    return result


# ------------------------------
# Somma totale delle fonti di finanziamento SPECIFICHE
# ------------------------------
def specific_funds_contribution(filters):
    projects_qs, funding_qs = get_filtered_projects_by_filters(filters)

    field_mapping = {
        "eu_funds_fesr": "FESR_UE",
        "eu_funds_fse": "FSE_UE",
        "eu_funds_feasr": "FEASR_UE",
        "eu_funds_feamp": "FEAMP_UE",
        "eu_funds_iog": "IOG_UE",
        "state_fsc": "FSC_Stato",
        "state_rotating_fund": "Fondo_di_Rotazione_Stato",
        "state_pac": "PAC_Stato",
        "state_completions": "Completamenti_Stato",
        "state_other_measures": "Altri_Stato",
        "regional_funds": "Regioni",
        "private_funds": "Privato",
        "municipal_funds": "Comune",
        "provincial_funds": "Provincia",
        "other_public_funds": "Altro_Pubblico"
    }

    # Aggrega solo i campi filtrati se funding_source è specificato
    funding_source = filters.get("funding_source")
    source_fields_map = {
        "UE": ["eu_funds_fesr", "eu_funds_fse", "eu_funds_feasr", "eu_funds_feamp", "eu_funds_iog"],
        "Stato": ["state_fsc", "state_rotating_fund", "state_pac", "state_completions", "state_other_measures"],
        "Regioni": ["regional_funds"],
        "Privato": ["private_funds"],
        "Comune": ["municipal_funds"],
        "Provincia": ["provincial_funds"],
        "Altro_Pubblico": ["other_public_funds"]
    }

    if funding_source in source_fields_map:
        fields_to_aggregate = source_fields_map[funding_source]
    else:
        fields_to_aggregate = list(field_mapping.keys())

    agg = funding_qs.aggregate(**{f: Sum(f) for f in fields_to_aggregate})

    # Mantieni tutte le chiavi per il serializer
    result = {v: 0.0 for v in field_mapping.values()}
    for f, out_key in field_mapping.items():
        if f in fields_to_aggregate:
            result[out_key] = float(agg.get(f, 0) or 0)
    return result


# ------------------------------
# Top 10 tematiche con il maggior valore di finanziamento (aggiornata con filtro funding_source)
# ------------------------------
def top10_thematic_objectives(filters):
    projects_qs, funding_qs = get_filtered_projects_by_filters(filters)

    # Se non ci sono progetti o finanziamenti filtrati, ritorna vuoto
    if not funding_qs.exists():
        return []

    themes = (
        funding_qs
        .values("project__oc_synthetic_theme")
        .annotate(amount=Sum("total_funds_gross"))
        .order_by("-amount")[:10]
    )

    return [
        {
            "description": t["project__oc_synthetic_theme"] or "Non specificato",
            "amount": float(t["amount"] or 0)
        }
        for t in themes
    ]


# ------------------------------
# Totale fondi da trovare (gap)
# ------------------------------
def get_funds_to_be_found(filters):
    projects_qs, funding_qs = get_filtered_projects_by_filters(filters)

    project_sums = funding_qs.values("project_id").annotate(total_savings=Sum("total_savings"))

    number_of_projects_with_gap = sum(1 for p in project_sums if p["total_savings"] > 0)
    total_missing_amount = sum(p["total_savings"] for p in project_sums if p["total_savings"] > 0)

    return {
        "number_of_projects_with_gap": number_of_projects_with_gap,
        "total_missing_amount": total_missing_amount
    }


# ------------------------------
# Realizzazione e pagamento - NON filtrata
# ------------------------------
def get_payments_realization_gap(filters):
    aggregation = Funding.objects.aggregate(
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


# ------------------------------
# Top 10 tipologie di progetto per finanziamento (aggiornata con filtro funding_source)
# ------------------------------
def get_top_project_typologies(filters):
    projects_qs, funding_qs = get_filtered_projects_by_filters(filters)

    # Se non ci sono progetti o finanziamenti filtrati, ritorna vuoto
    if not funding_qs.exists():
        return []

    typologies = (
        funding_qs
        .filter(project__cup_typology__isnull=False)
        .values("project__cup_typology")
        .annotate(total=Sum("total_funds_gross"))
        .order_by("-total")[:10]
    )

    return [
        {
            "type": t["project__cup_typology"] or "sconosciuto",
            "amount": float(t["total"] or 0)
        }
        for t in typologies
    ]