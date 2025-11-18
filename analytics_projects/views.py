# views.py
from django.db.models import Sum, F, Value, Case, When
from django.db.models.functions import Coalesce
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Project, Funding
from .serializers import SectorFundingSerializer


class TopSectorsAPIView(APIView):

    def get(self, request):

        project_funding = Funding.objects.values(
            project_id=F("project__local_project_code"),
            sector=Case(
                When(project__cup_descr_sector__isnull=False, project__cup_descr_sector__gt="",
                     then=F("project__cup_descr_sector")),
                default=F("project__oc_synthetic_theme")
            )
        ).annotate(
            total_financing=(
                Coalesce(F("total_funds_gross"), Value(0.0))
            )
        )

        aggregated = (
            project_funding
            .values("sector")
            .annotate(total_financing=Sum("total_financing"))
            .order_by("-total_financing")[:3]
        )

        data = SectorFundingSerializer(aggregated, many=True).data

        return Response({
            "TopSectors": data
        })