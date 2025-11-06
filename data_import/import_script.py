import csv
import logging
import os
from django.db import transaction
from analytics_projects.models import Project, Funding, Location

# Imposta il modulo settings del progetto
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Horizon_Analytics.settings")

# === Configurazione logging ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === Percorso del CSV ===
file_path = "../progetti_esteso_2021-2027_20250630.csv"


def safe_float(value):
    """
    Converte in float gestendo valori nulli, 'N/A' o vuoti.
    Sostituisce eventuali virgole con punti.
    """
    try:
        if value in (None, "", "N/A", "NULL"):
            return 0.0
        return float(str(value).replace(",", "."))
    except (ValueError, TypeError):
        return 0.0


def clean_str(value):
    """Pulisce stringhe da spazi o valori nulli."""
    return value.strip() if isinstance(value, str) else value



# === Lettura CSV ===
def import_projects_from_csv(file_path: str):
    """
    Legge un file CSV e restituisce una lista di dizionari con i dati.
    """
    projects_data = []

    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=";")
        for row in reader:
            projects_data.append({k: clean_str(v) for k, v in row.items()})

    logger.info(f"Importati {len(projects_data)} record dal file {file_path}")
    return projects_data


# === Importazione nel database ===
@transaction.atomic
def load_projects_into_db(projects_data):
    """
    Importa i progetti dal CSV associandoli alle sole regioni.
    Ogni regione è una Location univoca (nessun duplicato).
    """
    for data in projects_data:
        # === PROJECT ===
        project, _ = Project.objects.update_or_create(
            local_project_code=data["COD_LOCALE_PROGETTO"],
            defaults={
                "oc_project_status": data.get("OC_STATO_PROGETTO") or "Non applicabile",
                "oc_procedural_state": data.get("OC_STATO_PROCEDURALE") or "Non avviato",
                "oc_project_title": data.get("OC_TITOLO_PROGETTO", "Titolo non disponibile"),
                "cup_descr_sector": data.get("CUP_DESCR_SETTORE"),
                "oc_synthetic_theme": data.get("OC_TEMA_SINTETICO"),
            },
        )

        # === REGION LOCATION ===
        region_code = (data.get("COD_REGIONE") or "").strip()
        region_name = (data.get("DEN_REGIONE") or "").strip()
        macroarea = data.get("OC_MACROAREA", "ALTRO").strip().upper() or "ALTRO"

        # Se non c’è codice regione, assegna macroarea fittizia
        if not region_code:
            region_mapping = {
                "AMBITO NAZIONALE": ("000", "Ambito Nazionale"),
                "TRASVERSALE": ("001", "Ambito Trasversale"),
                "ESTERO": ("002", "Estero"),
                "MEZZOGIORNO": ("003", "Mezzogiorno"),
                "CENTRO-NORD": ("004", "Centro-Nord"),
                "ALTRO": ("099", "Altro non specificato"),
            }
            region_code, region_name = region_mapping.get(
                macroarea, ("099", "Altro non specificato")
            )

        # Crea o riusa la location
        location, created = Location.objects.get_or_create(
            common_code=region_code,
            defaults={
                "common_name": region_name,
                "province_code": "",
                "province_name": "",
                "region_code": region_code,
                "region_name": region_name,
                "macroarea": macroarea,
            },
        )

        # Aggiorna eventuali nomi più recenti
        if not created:
            changed = False
            for field in ["common_name", "region_name", "macroarea"]:
                new_val = locals()[field] if field in locals() else data.get(field)
                old_val = getattr(location, field)
                if new_val and old_val != new_val:
                    setattr(location, field, new_val)
                    changed = True
            if changed:
                location.save()

        # Collega il progetto alla regione
        project.locations.add(location)

        # === FUNDING ===
        Funding.objects.update_or_create(
            project=project,
            defaults={
                "eu_funds": safe_float(data.get("FINANZ_UE")),
                "total_funds_gross": safe_float(data.get("FINANZ_TOTALE_PUBBLICO")),
                "total_funds_net": safe_float(data.get("OC_FINANZ_TOT_PUB_NETTO")),
            },
        )

    logger.info("✅ Import completato: location basate solo su regioni create con successo.")
