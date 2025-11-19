from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import OverviewSerializer
from .services import *

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

        num_projects_with_status = count_projects_with_status(filters)
        macroarea_financing = funding_by_macroarea(filters)

        # Answer JSON
        data = {
            "filters": {
                "region": region,
                "macroarea": macroarea
            },

            "number_of_projects": num_projects_with_status['total'],
            "total_financing": sum_funding_gross(filters),
            "number_ended_projects": num_projects_with_status['concluded'],
            "number_not_started_projects": num_projects_with_status['not_started'],
            "number_projects_in_progress": num_projects_with_status['in_progress'],
            "number_projects_liquidated": num_projects_with_status['liquidated'],
            "middle_north_financing": macroarea_financing['Centro-Nord'],
            "midday_financing": macroarea_financing['Mezzogiorno'],
            "national_financing": macroarea_financing['Ambito Nazionale'],
            "abroad_financing": macroarea_financing['Estero'],
            "trasversal_financing": macroarea_financing['Trasversale'],
            "top_projects": top_10_projects(filters),
            "number_big_projects": count_big_projects(filters),
            "top_sectors": get_top_sectors(filters)
        }

        serializer = OverviewSerializer(data)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
    
