from django.shortcuts import render
from django.http import HttpResponse


def dashboard(request):
    return render(request, 'analytics_projects/dashboard.html')


def import_csv(request):
    if request.method == 'POST':
        return HttpResponse("CSV importato con successo!")
    return render(request, 'analytics_projects/import_csv.html')
