from django.urls import path
from .views import DashboardAPIView

urlpatterns = [
    path('api/dashboard/', DashboardAPIView.as_view(), name='api-dashboard'), #url of API
]

