from django.urls import path
from .views import TopSectorsAPIView

urlpatterns = [
    path("api/top-sectors/", TopSectorsAPIView.as_view(), name="top-sectors")
]
