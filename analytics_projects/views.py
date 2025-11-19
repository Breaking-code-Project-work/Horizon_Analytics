from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import OverviewSerializer
from .services import get_top_sectors


class OverviewAPI(APIView):

    def get(self, request):

        region = request.query_params.get("region")
        macroarea = request.query_params.get("macroarea")

        filters = {
            "region": region,
            "macroarea": macroarea
        }

        data = {
            "top_sectors": get_top_sectors(filters),
        }

        serializer = OverviewSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        return Response({"data": serializer.data}, status=status.HTTP_200_OK)