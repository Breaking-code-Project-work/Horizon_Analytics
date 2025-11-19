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


