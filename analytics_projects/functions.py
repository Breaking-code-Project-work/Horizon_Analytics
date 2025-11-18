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

#Functions that give top 10 projects for financing

#Function that give number of big projects

#Function that give top 3 sectors


