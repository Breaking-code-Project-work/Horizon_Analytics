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
from serializers import OverviewSerializer
from services import *

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

        numProjectswithstatus = countProjectsWithStatus(filters)
        macroareaFinancing = fundingByMacroarea(filters)

        # Answer JSON
        data = {
            "filters": {
                "region": region,
                "macroarea": macroarea
            },

            "numProjects": countProjects(filters),
            "totalFinancing": numProjectswithstatus['total'],
            "numberEndedProjects": numProjectswithstatus['concluded'],
            "numberNotStartedProjects": numProjectswithstatus['not_started'],
            "numberProjectsInProgress": numProjectswithstatus['in_progress'],
            "numberProjectsLiquidated": numProjectswithstatus['liquidated'],
            "middleNorthFinancing": macroareaFinancing['Centro-Nord'],
            "middayFinancing": macroareaFinancing['Mezzogiorno'],
            "nationalFinancing": macroareaFinancing['Ambito Nazionale'],
            "abroadFinancing": macroareaFinancing['Estero'],
            "trasversalFinancing": macroareaFinancing['Trasversale'],
            "topProjects": top10Projects(filters),
            "numberBigProjects": countBigProjects(filters),
            "topSectors": get_top_sectors(filters)
        }

        serializer = OverviewSerializer(data)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
    
