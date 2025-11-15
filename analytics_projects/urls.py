from django.urls import path
from .views import OverviewAPI
from . import views

urlpatterns = [
    path('api/overview/', OverviewAPI.as_view(), name='overview-api'), #url of API
    path('dashboard/', views.dashboard, name='dashboard'), #url of dashboard
    path('import/', views.import_csv, name='import_csv'),
]
