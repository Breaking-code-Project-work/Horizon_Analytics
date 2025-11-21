import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "horizon_analytics.settings")
django.setup()

from analytics_projects.models import Location

locations = [
    {"region_code": "001", "region_name": "PIEMONTE", "macroarea": "Centro-Nord"},
    {"region_code": "002", "region_name": "VALLE D'AOSTA", "macroarea": "Centro-Nord"},
    {"region_code": "003", "region_name": "LOMBARDIA", "macroarea": "Centro-Nord"},
    {"region_code": "004", "region_name": "TRENTINO-ALTO ADIGE", "macroarea": "Centro-Nord"},
    {"region_code": "005", "region_name": "VENETO", "macroarea": "Centro-Nord"},
    {"region_code": "006", "region_name": "FRIULI-VENEZIA GIULIA", "macroarea": "Centro-Nord"},
    {"region_code": "007", "region_name": "LIGURIA", "macroarea": "Centro-Nord"},
    {"region_code": "008", "region_name": "EMILIA-ROMAGNA", "macroarea": "Centro-Nord"},
    {"region_code": "009", "region_name": "TOSCANA", "macroarea": "Centro-Nord"},
    {"region_code": "010", "region_name": "UMBRIA", "macroarea": "Centro-Nord"},
    {"region_code": "011", "region_name": "MARCHE", "macroarea": "Centro-Nord"},
    {"region_code": "012", "region_name": "LAZIO", "macroarea": "Centro-Nord"},
    {"region_code": "013", "region_name": "ABRUZZO", "macroarea": "Mezzogiorno"},
    {"region_code": "014", "region_name": "MOLISE", "macroarea": "Mezzogiorno"},
    {"region_code": "015", "region_name": "CAMPANIA", "macroarea": "Mezzogiorno"},
    {"region_code": "016", "region_name": "PUGLIA", "macroarea": "Mezzogiorno"},
    {"region_code": "017", "region_name": "BASILICATA", "macroarea": "Mezzogiorno"},
    {"region_code": "018", "region_name": "CALABRIA", "macroarea": "Mezzogiorno"},
    {"region_code": "019", "region_name": "SICILIA", "macroarea": "Mezzogiorno"},
    {"region_code": "020", "region_name": "SARDEGNA", "macroarea": "Mezzogiorno"},
    {"region_code": "997", "region_name": "PAESI EUROPEI", "macroarea": "Estero"},
    {"region_code": "000", "region_name": "AMBITO NAZIONALE", "macroarea": "Ambito Nazionale"},
]

for loc in locations:
    Location.objects.update_or_create(
        region_code=loc["region_code"],
        defaults={
            "region_name": loc["region_name"],
            "macroarea": loc["macroarea"],
        }
    )

print("Locations caricate correttamente!")
