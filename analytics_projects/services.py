import os
import django
from django.db.models import Prefetch
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horizon_analytics.settings')
django.setup()

from analytics_projects.models import Project, Funding, Location

# ------------------------------
# Funzione base per filtrare progetti
# ------------------------------

def get_filtered_projects_analysis(filters):
    """
    filter by funding_source and macroarea
    """
    funding_source = filters.get("funding_source")
    macroarea = filters.get("macroarea")

    projects_qs = Project.objects.all()

    # Filtro per macroarea
    if macroarea and macroarea != "Tutte":
        projects_qs = projects_qs.filter(locations__macroarea=macroarea)

    # Prefetch dei funding in base al funding_source
    if funding_source and funding_source != "Tutte":
        # Definiamo il filtro dinamico sul funding
        # assumiamo che funding_source sia lo stesso nome del campo in Funding
        funding_prefetch = Prefetch(
            "funding",
            queryset=Funding.objects.only(
                funding_source,  # il campo specifico richiesto
                "total_funds_gross",
                "total_funds_net",
                "total_savings",
                "total_public_savings"
            ),
            to_attr="filtered_funding"
        )
        projects_qs = projects_qs.prefetch_related(funding_prefetch)
    else:
        # Tutti i funding
        projects_qs = projects_qs.prefetch_related("funding")

    return projects_qs.distinct()

def get_funds_to_be_found(filters):
    """
    Give a dictionary with:
    - number of projects with total savings > 0
    - total sum of savings of these projects
    """
    projects = get_filtered_projects_analysis(filters)

    # projects with total_savings > 0
    projects_with_savings = [p for p in projects if p.funding.total_savings > 0]

    number_of_projects_with_gap = len(projects_with_savings)
    total_missing_amount = sum(p.funding.total_savings for p in projects_with_savings)

    return {
        "number_of_projects_with_gap": number_of_projects_with_gap,
        "total_missing_amount": total_missing_amount
    }
