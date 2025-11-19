import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horizon_analytics.settings')

# Initialize Django
django.setup()

# import models
from analytics_projects.models import Project, Location, Funding

#to use sum on queries
from django.db.models import Sum

def countProjects(filters):
    '''Function that give number of projects'''
    projects = Project.objects.all()

    region = filters.get("region")
    if region and region != "nessun filtro":
        projects = projects.filter(locations__region_code=region).distinct()

    macroarea = filters.get("macroarea")
    if macroarea and macroarea != "nessun filtro":
        projects = projects.filter(locations__macroarea=macroarea).distinct()

    return projects.count()


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


