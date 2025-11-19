import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horizon_analytics.settings')

# Initialize Django
django.setup()

# import models
from analytics_projects.models import Project, Location, Funding

#to use sum on queries
from django.db.models import Sum
#Function that give number of projects 

#Function that give financing of projects 

#Function that give number of not started, ended and in progress projects

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

    top10Projects = {}
    for index, project in enumerate(projects, start=1):
        # all region in a string
        regions_str = ", ".join([loc.region for loc in project.locations.all()])
        # all macroaree in a string
        macroareas_str = ", ".join([loc.macroarea for loc in project.locations.all()])

        top10Projects[f"project{index}"] = {
            "id": project.id,
            "title": project.title,
            "totalFinancing": project.funding.total_financing,
            "region": regions_str,
            "macroarea": macroareas_str,
        }

    return top10Projects

#Function that give number of big projects

#Function that give top 3 sectors


#Function that give number of projects

#Function that give financing of projects

#Function that give number of not started, ended and in progress projects

#Functions that give top 10 projects for financing

#Function that give number of big projects
def countBigProjects(filters):
    big_project_threshold = 50_000_000
    projects = Project.objects.all()

    region = filters.get("region")
    if region and region != "nessun filtro":
        # Filtra progetti che hanno almeno una location con quel region_code
        projects = projects.filter(locations__region_code=region).distinct()

    macroarea = filters.get("macroarea")
    if macroarea and macroarea != "nessun filtro":
        projects = projects.filter(locations__macroarea=macroarea).distinct()

    # Progetti con total_funds_gross >= soglia
    projects = projects.filter(funding__total_funds_gross__gte=big_project_threshold).distinct()

    return projects.count()

#Function that give top 3 sectors

#Function that returns the finances given to a specific macroarea
def fundingByMacroarea(filters):
    fundings = Funding.objects.all()

    region = filters.get("region")
    if region and region != "nessun filtro":
        fundings = fundings.filter(project__locations__region_code=region)

    macroarea = filters.get("macroarea")
    if macroarea and macroarea != "nessun filtro":
        fundings = fundings.filter(project__locations__macroarea=macroarea)

    fundings = fundings.distinct()

    # Somma totale dei fondi per macroarea
    result = fundings.values("project__locations__macroarea").annotate(
        total=Sum("total_funds_gross")
    )

    return {
        item["project__locations__macroarea"]: item["total"] or 0
        for item in result
    }


#Function that give number of projects 

#Function that give financing of projects 

def countProjectsWithStatus(filters):
    '''Function that give number of not started, ended and in progress projects'''
    projects = Project.objects.all()

    # Filtri dinamici su location
    region = filters.get("region")
    if region and region != "nessun filtro":
        projects = projects.filter(locations__region_code=region).distinct()

    macroarea = filters.get("macroarea")
    if macroarea and macroarea != "nessun filtro":
        projects = projects.filter(locations__macroarea=macroarea).distinct()
    notStartedProjects = projects.filter(
        oc_project_status=Project.ProjectStatusChoices.NOT_STARTED
    ).distinct()

    inProgressProjects = projects.filter(
        oc_project_status=Project.ProjectStatusChoices.ONGOING
    ).distinct()

    concludedProjects = projects.filter(
        oc_project_status=Project.ProjectStatusChoices.CONCLUDED
    ).distinct()

    liquidatedProjects = projects.filter(
        oc_project_status=Project.ProjectStatusChoices.LIQUIDATED
    ).distinct()

        # give count of projects of all status
    return {
        "total": projects.count(),
        "not_started": notStartedProjects.count(),
        "in_progress": inProgressProjects.count(),
        "concluded": concludedProjects.count(),
        "liquidated": liquidatedProjects.count()
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

#Function that give number of not started, ended and in progress projects
   

#Functions that give top 10 projects for financing

#Function that give number of big projects

#Function that give top 3 sectors


