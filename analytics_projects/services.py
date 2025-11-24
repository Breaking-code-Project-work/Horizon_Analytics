import os
import django
from django.db.models import Sum

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

def get_top_project_typologies(filters):
    projects_qs = get_filtered_projects(filters)

    fundings = Funding.objects.filter(project__in=projects_qs) \
        .values("project__cup_typology") \
        .annotate(total=Sum("total_funds_gross")) \
        .order_by("-total")[:10]

    result = []
    for x in fundings:
        result.append({
            "typology": x["project__cup_typology"],
            "amount": x["total"] or 0
        })

    return result
