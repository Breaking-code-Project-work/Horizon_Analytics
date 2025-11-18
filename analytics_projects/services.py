from django.db.models import Sum
from models.project import Project, Funding

def get_top_sectors(filters):
    qs = Funding.objects.filter(
        project__in=Project.objects.filter(**filters)
    ).values(
        "project__cup_descr_sector"
    ).annotate(
        total=Sum("total_funds_gross")
    ).order_by("-total")[:3]

    return [{"sector": x["project__cup_descr_sector"], "total": x["total"]} for x in qs]