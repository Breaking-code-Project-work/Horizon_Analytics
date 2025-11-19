from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from serializers import OverviewSerializer
from services import *

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
    
