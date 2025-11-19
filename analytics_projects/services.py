import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horizon_analytics.settings')

# Initialize Django
django.setup()

# import models
from analytics_projects.models import Project, Location, Funding

#to use sum on queries
from django.db.models import Sum

def get_top_sectors(filters):
    '''function that give top 3 sectors'''
    projects = Funding.objects.filter(
        project__in=Project.objects.filter(**filters)
    ).values(
        "project__cup_descr_sector"
    ).annotate(
        total=Sum("total_funds_gross")
    ).order_by("-total")[:3]

    result = {}

    for i, x in enumerate(projects, start=1):
        result[f"Sector{i}"] = {
            "name": x["project__cup_descr_sector"],
            "total_financing": x["total"]
        }

    return result

def top10Projects(filters):
    '''Function that returns top 10 projects by financing'''

    projects = Project.objects.select_related("funding").prefetch_related("locations")

    region = filters.get("region")
    if region and region != "nessun filtro":
        projects = projects.filter(locations__region_code=region)

    macroarea = filters.get("macroarea")
    if macroarea and macroarea != "nessun filtro":
        projects = projects.filter(locations__macroarea=macroarea)

    # ---- order by DESC and pick first 10 ----
    projects = projects.order_by("-funding__total_financing")[:10]

    top_10_projects = {}
    for index, project in enumerate(projects, start=1):
        # all region in a string
        regions_str = ", ".join([loc.region for loc in project.locations.all()])
        # all macroaree in a string
        macroareas_str = ", ".join([loc.macroarea for loc in project.locations.all()])

        top_10_projects[f"project{index}"] = {
            "id": project.id,
            "title": project.title,
            "total_financing": project.funding.total_financing,
            "region": regions_str,
            "macroarea": macroareas_str,
        }

    return top_10_projects

def countBigProjects(filters):
    '''Function that give number of big projects'''
    big_project_threshold = 50_000_000
    projects = Project.objects.all()

    region = filters.get("region")
    if region and region != "nessun filtro":
        # Filter projects by region code
        projects = projects.filter(locations__region_code=region).distinct()

    macroarea = filters.get("macroarea")
    if macroarea and macroarea != "nessun filtro":
        projects = projects.filter(locations__macroarea=macroarea).distinct()

    # total_funds_gross >= 50 000 000
    projects = projects.filter(funding__total_funds_gross__gte=big_project_threshold).distinct()

    return projects.count()

def fundingByMacroarea(filters):
    '''Function that returns the finances given to a specific macroarea'''
    fundings = Funding.objects.all()

    region = filters.get("region")
    if region and region != "nessun filtro":
        fundings = fundings.filter(project__locations__region_code=region)

    macroarea = filters.get("macroarea")
    if macroarea and macroarea != "nessun filtro":
        fundings = fundings.filter(project__locations__macroarea=macroarea)

    fundings = fundings.distinct()

    # total sum of macroarea
    result = fundings.values("project__locations__macroarea").annotate(
        total=Sum("total_funds_gross")
    )

    return {
        item["project__locations__macroarea"]: item["total"] or 0
        for item in result
    }

def countProjectsWithStatus(filters):
    '''Function that give number of not started, ended and in progress projects'''
    projects = Project.objects.all()

    # filters
    region = filters.get("region")
    if region and region != "nessun filtro":
        projects = projects.filter(locations__region_code=region).distinct()

    macroarea = filters.get("macroarea")
    if macroarea and macroarea != "nessun filtro":
        projects = projects.filter(locations__macroarea=macroarea).distinct()
    not_started_projects = projects.filter(
        oc_project_status=Project.ProjectStatusChoices.NOT_STARTED
    ).distinct()

    in_progress_projects = projects.filter(
        oc_project_status=Project.ProjectStatusChoices.ONGOING
    ).distinct()

    concluded_projects = projects.filter(
        oc_project_status=Project.ProjectStatusChoices.CONCLUDED
    ).distinct()

    liquidated_projects = projects.filter(
        oc_project_status=Project.ProjectStatusChoices.LIQUIDATED
    ).distinct()

        # give count of projects of all status
    return {
        "total": projects.count(),
        "not_started": not_started_projects.count(),
        "in_progress": in_progress_projects.count(),
        "concluded": concluded_projects.count(),
        "liquidated": liquidated_projects.count()
    }

def sumFundingGross(filters):
    '''Function that give financing of projects'''
    fundings = Funding.objects.all()

    region = filters.get("region")
    macroarea = filters.get("macroarea")

    if region and region != "nessun filtro":
        fundings = fundings.filter(project__locations__region_code=region)

    if macroarea and macroarea != "nessun filtro":
        fundings = fundings.filter(project__locations__macroarea=macroarea)

    fundings = fundings.distinct()

    result = fundings.aggregate(total_gross=Sum('total_funds_gross'))

    return result['total_gross'] or 0
