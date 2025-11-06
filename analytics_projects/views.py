# analytics_projects/views.py
from django.shortcuts import render
from django.http import HttpResponse
#import per testing con Pandas
import csv
import io
import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse

def import_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES.get('file')
        if not csv_file.name.endswith('.csv'):
            return HttpResponse("Errore: il file deve essere un CSV.")

        # Legge il file CSV
        data = csv_file.read().decode('utf-8')
        io_string = io.StringIO(data)
        reader = csv.reader(io_string, delimiter=',')

        # Legge le righe
        rows = list(reader)

        # Mostra a video le prime 5 righe
        return HttpResponse(f"CSV importato con successo!<br><br>Prime 5 righe:<br>{rows[:5]}")

    return render(request, 'analytics_projects/import_csv.html')

def dashboard(request):
    return render(request, 'analytics_projects/dashboard.html')

def import_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES.get('file')
        if not csv_file.name.endswith('.csv'):
            return HttpResponse("Errore: il file deve essere un CSV.")

        # 🔹 Legge il CSV con pandas
        df = pd.read_csv(csv_file, sep=";", decimal=",", encoding="utf-8")

        # 🔹 Mostra le colonne trovate
        columns = df.columns.tolist()
        columns_html = "<br>".join(columns)

        # 🔹 Mostra anche le prime righe
        html_preview = df.head(5).to_html()

        return HttpResponse(
            f"""
            ✅ <b>CSV importato con successo!</b><br><br>
            <b>Colonne trovate:</b><br>{columns_html}<br><br>
            <b>Prime 5 righe:</b><br>{html_preview}
            """
        )

    return render(request, 'analytics_projects/import_csv.html')
