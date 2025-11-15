from django.urls import path
from .views import OverviewAPI

urlpatterns = [
    path('api/overview/', OverviewAPI.as_view(), name='overview-api'), #url of API
]

