import os

# Setup Django 
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "horizon_analytics.settings")
import django
django.setup()

import glob, logging, csv 

from django.db import transaction
from analytics_projects.models import Project, Funding, Location

# Logging 
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Path CSV 
file_path = "../progetti_esteso_2021-2027_20250630.csv"


# float normalize
def safe_float(value):
    """Converte valori in float gestendo vuoti, N/A, NULL."""
    try:
        if value in (None, "", "N/A", "NULL"):
            return 0.0
        return float(str(value).replace(",", "."))
    except (ValueError, TypeError):
        return 0.0


def clean_str(value):
    """Rimuove spazi iniziali/finali da stringhe."""
    return value.strip() if isinstance(value, str) else value

# CSV reading
def import_projects_from_csv(file_path: str):
    """Legge un file CSV e restituisce una lista di dizionari con i dati."""
    projects_data = []
    with open(file_path, mode="r", encoding="utf-8-sig") as file:  # <- usa utf-8-sig per BOM
        reader = csv.DictReader(file, delimiter=";")
        for row in reader:
            # rimuove virgolette dai nomi delle colonne e dai valori
            clean_row = {k.strip().strip('"'): clean_str(v).strip('"') for k, v in row.items()}
            projects_data.append(clean_row)
    logger.info(f"Importati {len(projects_data)} record dal file {file_path}")
    return projects_data

# multiple CSV reading
def import_multiple_csv(folder_path: str):
    """
    Importa tutti i CSV in una cartella con la stessa intestazione.
    Restituisce una lista unica di dizionari, saltando le intestazioni duplicate.
    """
    all_data = []
    csv_files = sorted(glob.glob(f"{folder_path}/*.csv"))  # All csv

    for i, file_path in enumerate(csv_files):
        with open(file_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=";")
            rows = list(reader)
            logger.info(f"Importati {len(rows)} record da {file_path}")
            all_data.extend(rows)  # concatenate all lines
    logger.info(f"Totale record importati da tutti i CSV: {len(all_data)}")
    return all_data


# Normalize csv
def normalize_projects_data(projects_data):
    normalized_data = []
    DELIMITER = ":::"
    for data in projects_data:
        region_codes = str(data.get("COD_REGIONE", "") or "").split(DELIMITER)
        region_names = str(data.get("DEN_REGIONE", "") or "").split(DELIMITER)

        # no multiple regions
        if len(region_codes) == 1 and len(region_names) == 1:
            normalized_data.append(data)
            continue

        # duplicate rows
        for code, name in zip(region_codes, region_names):
            new_row = data.copy()
            new_row["COD_REGIONE"] = code.strip()
            new_row["DEN_REGIONE"] = name.strip()
            normalized_data.append(new_row)

    logger.info(f"Normalizzazione completata: {len(projects_data)} → {len(normalized_data)} righe")
    return normalized_data


# Import on database 
@transaction.atomic
def load_projects_into_db(projects_data):
    for data in projects_data:
        # PROJECT 
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

        # FUNDING
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
    # LOCATION
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

if __name__ == "__main__":
    projects = import_projects_from_csv("csv/Progetti_2021-2027_1.csv")  # percorso relativo del CSV
    #projects = import_multiple_csv("csv") #path folder
    print(projects[0].keys())
    normalized_projects = normalize_projects_data(projects)
    load_projects_into_db(normalized_projects)