from django.urls import path
from .views import OverviewAPI, AnalysisAPI

urlpatterns = [
    path('api/overview/', OverviewAPI.as_view(), name='overview-api'), #url of API
    path('api/analysis/', AnalysisAPI.as_view(), name='analysis-api'), #url of API
]

