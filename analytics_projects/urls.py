from django.urls import path
from .views import OverviewAPI

urlpatterns = [
    path("api/top-sectors/", OverviewAPI.as_view(), name="top-sectors")
]
