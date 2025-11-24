from django.urls import path
from django.contrib import admin
from . import views
from .views import OverviewAPI, AnalysisAPI

urlpatterns = [
    path('api/overview/', OverviewAPI.as_view(), name='overview-api'), #url of API
    path('admin/', admin.site.urls),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('visione_di_insieme_page/', views.visione_di_insieme_page, name='visione_di_insieme_page'), #url of visione d'insieme
    path('analisi_finanziaria_page/', views.analisi_finanziaria_page, name='analisi_finanziaria_page'), #url of analisi finanziaria
    path('analisi_settoriale_page/', views.analisi_settoriale_page, name='analisi_settoriale_page'), #url of analisi settoriale
    path('anomalie_page/', views.anomalie_page, name='anomalie_page'), #url of anomalie page
    path('beneficiari_page/', views.beneficiari_page, name='beneficiari_page'), #url of beneficiari page
    path('efficienza_e_performance_page/', views.efficienza_e_performance_page, name='efficienza_e_performance_page'), #url of efficenza e performance page
    path('territori_e_attori_page/', views.territori_e_attori_page, name='territori_e_attori_page'), #url of territori e attori page
    path('api/analysis/', AnalysisAPI.as_view(), name='analysis-api'), #url of API
]
