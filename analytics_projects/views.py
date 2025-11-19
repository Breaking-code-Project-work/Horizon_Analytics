from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import OverviewSerializer
from .services import get_top_sectors


class OverviewAPI(APIView):
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
#here go the import for backend script

def dashboard(request):
    return render(request, 'analytics_projects/dashboard.html')

def visione_di_insieme_page(request):
    return render(request, 'analytics_projects/visione_di_insieme_page.html')

def analisi_finanziaria_page(request):
    return render(request, 'analytics_projects/analisi_finanziaria_page.html')

def analisi_settoriale_page(request):
    return render(request, 'analytics_projects/analisi_settoriale_page.html')

def anomalie_page(request):
    return render(request, 'analytics_projects/anomalie_page.html')

def beneficiari_page(request):
    return render(request, 'analytics_projects/beneficiari_page.html')

def efficienza_e_performance_page(request):
    return render(request, 'analytics_projects/efficienza_e_performance_page.html')

def territori_e_attori_page(request):
    return render(request, 'analytics_projects/territori_e_attori_page.html')

def import_csv(request):
    if request.method == 'POST':
        return HttpResponse("CSV importato con successo!")
    return render(request, 'analytics_projects/import_csv.html')

class OverviewAPI(APIView):
    """
    API that recieve filters from frontend and give as output a Jason called data
    """
    def get(self, request):
        # Recover filters from query string
        region = request.query_params.get("region")
        macroarea = request.query_params.get("macroarea")
        filters = {
            "region": region,
            "macroarea": macroarea
        }

        # variabiles of back end
        numProjects = 1
        totalFinancing = 1
        numberEndedProjects = 1
        numberNotStartedProjects = 1
        numberProjectsInProgress = 1
        MiddayFinancing = 1
        MiddleNorthFinancing = 1
        numberBigProjects = 1

        Project1 = []
        Project2 = []
        Project3 = []
        Project4 = []
        Project5 = []
        Project6 = []
        Project7 = []
        Project8 = []
        Project9 = []
        Project10 = []

        Sector1 = []
        Sector2 = []
        Sector3 = []
        # Answer JSON
        response_data = {
             "data": {
                "filters": {
                    "region": region,
                    "macroarea": macroarea
                },

                "numProjects": numProjects,
                "totalFinancing": totalFinancing,
                "numberEndedProjects": numberEndedProjects,
                "numberNotStartedProjects": numberNotStartedProjects,
                "numberProjectsInProgress": numberProjectsInProgress,
                "MiddayFinancing": MiddayFinancing,
                "MiddleNorthFinancing": MiddleNorthFinancing,
                "TopProjects": {
                    "Project1": Project1,
                    "Project2": Project2,
                    "Project3": Project3,
                    "Project4": Project4,
                    "Project5": Project5,
                    "Project6": Project6,
                    "Project7": Project7,
                    "Project8": Project8,
                    "Project9": Project9,
                    "Project10": Project10
                    },
                "numberBigProjects": numberBigProjects,
                "TopSectors": {
                    "Sector1": Sector1,
                    "Sector2": Sector2,
                    "Sector3": Sector3
                }
            }
        }

        return Response(response_data, status=status.HTTP_200_OK)

