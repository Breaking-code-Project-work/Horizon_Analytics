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
    '''Functions that give top 10 projects for financing'''
    index = 0
    # projects row with join with funding and location 
    projects = Project.objects.select_related("funding", "location")

    region = filters.get("region")
    if region and region != "nessun filtro":
        projects = projects.filter(location__region=region)

    macroarea = filters.get("macroarea")
    if macroarea and macroarea != "nessun filtro":
        projects = projects.filter(location__macroarea=macroarea)

    # ---- order by financing Desc ----
    projects = projects.order_by("-funding__total_financing")

    # ---- limit 10 ----
    projects = projects[:10]

    # ---- build the output ----
    result = {"TopProjects": {}}

    for project in projects:
        index += 1   

        result["TopProjects"][f"Project{index}"] = {
            "id": project.id,
            "Title": project.title,
            "TotalFinancing": project.funding.total_financing,
            "Region": project.location.region,
            "Macroarea": project.location.macroarea,
        }

    return result

#Function that give number of big projects

#Function that give top 3 sectors


