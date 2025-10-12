from django.http import HttpResponse


def home(request):
    return HttpResponse("Benvenuto su Horizon Analytics!")
