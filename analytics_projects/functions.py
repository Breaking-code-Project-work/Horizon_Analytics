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