from django.contrib import admin
from .models import Project, Location, Funding

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('local_project_code', 'oc_project_title', 'oc_project_status', 'cup_typology', 'oc_synthetic_theme', 'is_trasversale')
    search_fields = ('local_project_code', 'oc_project_title')
    list_filter = ('is_trasversale',)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('region_code', 'region_name', 'macroarea')
    search_fields = ('region_name',)

@admin.register(Funding)
class FundingAdmin(admin.ModelAdmin):
    list_display = ('project', 'total_funds_gross', 'total_funds_net')
    search_fields = ('project__oc_project_title',)
