from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import OverviewSerializer, AnalysisSerializer
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
    API that receives filters from frontend and returns a JSON called data
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

        # Prepare JSON
        data = {
            "filters": {
                "region": region,
                "macroarea": macroarea
            },
            "number_of_projects": num_projects_with_status.get('total', 0),
            "total_financing": sum_funding_gross(filters),
            "number_ended_projects": num_projects_with_status.get('concluded', 0),
            "number_not_started_projects": num_projects_with_status.get('not_started', 0),
            "number_projects_in_progress": num_projects_with_status.get('in_progress', 0),
            "number_projects_liquidated": num_projects_with_status.get('liquidated', 0),
            "middle_north_financing": macroarea_financing.get('Centro-Nord', 0.0),
            "midday_financing": macroarea_financing.get('Mezzogiorno', 0.0),
            "national_financing": macroarea_financing.get('Ambito Nazionale', 0.0),
            "abroad_financing": macroarea_financing.get('Estero', 0.0),
            "top_projects": top_10_projects(filters),
            "number_big_projects": count_big_projects(filters),
            "top_sectors": get_top_sectors(filters)
        }

        # Pass the already-prepared dictionary directly to the serializer
        serializer = OverviewSerializer(data)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

class AnalysisAPI(APIView):
    """
    API that receives filters from frontend and returns
    the JSON structure of the Contract API.
    """

    def get(self, request):
        # Recover filters from query parameters
        macroarea = request.query_params.get("macroarea")
        funding_source = request.query_params.get("funding_source")

        filters = {
            "macroarea": macroarea,
            "funding_source": funding_source
        }

        data = {
            "filters": {
                "macroarea": macroarea,
                "funding_source": funding_source
            },
            "data": {
                "funding_sources_analysis": funding_sources_analysis(filters),
                "specific_funds_contribution": specific_funds_contribution(filters),
                "top10_thematic_objectives": top10_thematic_objectives(filters),
                "top10_project_typologies": get_top_project_typologies(),
                "funds_to_be_found": get_funds_to_be_found(filters),
                "payments_realization_gap": get_payments_realization_gap(filters),
            }
        }
        # Pass the already-prepared dictionary directly to the serializer
        serializer = AnalysisSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)

