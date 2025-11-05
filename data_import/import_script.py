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
    Carica i dati letti dal CSV nel database Django.
    Usa transazioni atomiche per garantire la coerenza.
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

        # === LOCATION ===
        if data.get("COD_COMUNE"):
            location, _ = Location.objects.get_or_create(
                common_code=data["COD_COMUNE"],
                defaults={
                    "common_name": data.get("DEN_COMUNE", "Sconosciuto"),
                    "province_code": data.get("COD_PROVINCIA", ""),
                    "province_name": data.get("DEN_PROVINCIA", ""),
                    "region_code": data.get("COD_REGIONE", ""),
                    "region_name": data.get("DEN_REGIONE", ""),
                    "macroarea": data.get("OC_MACROAREA", "ALTRO"),
                },
            )
            # Collega la location al progetto (ManyToMany)
            project.locations.add(location)

        # === FUNDING ===
        Funding.objects.update_or_create(
            project=project,
            defaults={
                "eu_funds": safe_float(data.get("FINANZ_UE")),
                "eu_funds_fesr": safe_float(data.get("FINANZ_UE_FESR")),
                "eu_funds_fse": safe_float(data.get("FINANZ_UE_FSE")),
                "eu_funds_feasr": safe_float(data.get("FINANZ_UE_FEASR")),
                "eu_funds_feamp": safe_float(data.get("FINANZ_UE_FEAMP")),
                "eu_funds_iog": safe_float(data.get("FINANZ_UE_IOG")),
                "state_rotating_fund": safe_float(data.get("FINANZ_STATO_FONDO_DI_ROTAZIONE")),
                "state_fsc": safe_float(data.get("FINANZ_STATO_FSC")),
                "state_pac": safe_float(data.get("FINANZ_STATO_PAC")),
                "state_completions": safe_float(data.get("FINANZ_STATO_COMPLETAMENTI")),
                "state_other_measures": safe_float(data.get("FINANZ_STATO_ALTRI_PROVVEDIMENTI")),
                "regional_funds": safe_float(data.get("FINANZ_REGIONE")),
                "provincial_funds": safe_float(data.get("FINANZ_PROVINCIA")),
                "municipal_funds": safe_float(data.get("FINANZ_COMUNE")),
                "freed_resources": safe_float(data.get("FINANZ_RISORSE_LIBERATE")),
                "other_public_funds": safe_float(data.get("FINANZ_ALTRO_PUBBLICO")),
                "foreign_state": safe_float(data.get("FINANZ_STATO_ESTERO")),
                "private_funds": safe_float(data.get("FINANZ_PRIVATO")),
                "funds_to_find": safe_float(data.get("FINANZ_DA_REPERIRE")),
                "total_savings": safe_float(data.get("ECONOMIE_TOTALI")),
                "total_public_savings": safe_float(data.get("ECONOMIE_TOTALI_PUBBLICHE")),
                "total_funds_gross": safe_float(data.get("FINANZ_TOTALE_PUBBLICO")),
                "total_funds_net": safe_float(data.get("OC_FINANZ_TOT_PUB_NETTO")),
            },
        )

    logger.info("Tutti i progetti sono stati caricati nel database con successo")