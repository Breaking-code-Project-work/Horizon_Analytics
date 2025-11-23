import os
import django
from django.db.models import Sum
from django.db.models import Prefetch
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horizon_analytics.settings')
django.setup()

from analytics_projects.models import Project, Funding, Location

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

def get_payments_realization_gap(filters):
    """
    give a dictionary with total realized cost, total payment and difference between them
    """
    # no filters
    projects = Project.objects.all()

    # Aggrega i valori dei finanziamenti dei progetti filtrati
    aggregation = Funding.objects.filter(project__in=projects).aggregate(
        total_realized_cost=Sum('total_funds_gross'),
        total_payments_made=Sum('total_funds_net'),
    )

    total_realized_cost = aggregation['total_realized_cost'] or 0
    total_payments_made = aggregation['total_payments_made'] or 0
    overall_difference = total_realized_cost - total_payments_made

    return {
        "total_realized_cost": total_realized_cost,
        "total_payments_made": total_payments_made,
        "overall_difference": overall_difference
    }
