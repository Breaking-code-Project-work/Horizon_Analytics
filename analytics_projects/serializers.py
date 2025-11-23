from rest_framework import serializers

#Overview
class FiltersOverviewSerializer(serializers.Serializer):
    region = serializers.CharField()
    macroarea = serializers.CharField()

class ProjectSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    total_financing = serializers.FloatField()
    region = serializers.CharField()
    macroarea = serializers.CharField()

class TopProjectsSerializer(serializers.DictField):
    def __init__(self, *args, **kwargs):
        kwargs['child'] = ProjectSerializer()
        super().__init__(*args, **kwargs)

class SectorSerializer(serializers.Serializer):
    name = serializers.CharField()
    total_financing = serializers.FloatField()

class TopSectorsSerializer(serializers.DictField):
    def __init__(self, *args, **kwargs):
        kwargs['child'] = SectorSerializer()
        super().__init__(*args, **kwargs)

# -----------------------------
# Overview Analysis (MAIN BLOCK)
# -----------------------------
class OverviewSerializer(serializers.Serializer):
    filters = FiltersOverviewSerializer()
    number_of_projects = serializers.IntegerField()
    total_financing = serializers.FloatField()
    number_ended_projects = serializers.IntegerField()
    number_not_started_projects = serializers.IntegerField()
    number_projects_in_progress = serializers.IntegerField()
    midday_financing = serializers.FloatField()
    middle_north_financing = serializers.FloatField()
    national_financing = serializers.FloatField()
    abroad_financing = serializers.FloatField()
    top_projects = TopProjectsSerializer()
    number_big_projects = serializers.IntegerField()
    top_sectors = TopSectorsSerializer()

#Financing analysis

class AnalysisFiltersSerializer(serializers.Serializer):
    macroarea = serializers.CharField()
    funding_source = serializers.CharField()

class FundingSourcesAnalysisSerializer(serializers.Serializer):
    UE = serializers.FloatField()
    Stato = serializers.FloatField()
    Regioni = serializers.FloatField()
    Privato = serializers.FloatField()
    Comune = serializers.FloatField()
    Altro_Pubblico = serializers.FloatField()
    Provincia = serializers.FloatField()

class SpecificFundsContributionSerializer(serializers.Serializer):
    FESR_UE = serializers.FloatField()
    FSE_UE = serializers.FloatField()
    FSC_Stato = serializers.FloatField()
    Fondo_di_Rotazione_Stato = serializers.FloatField()
    FEASR_UE = serializers.FloatField()
    FEAMP_UE = serializers.FloatField()
    IOG_UE = serializers.FloatField()
    PAC_Stato = serializers.FloatField()
    Completamenti_Stato = serializers.FloatField()
    Altri_Stato = serializers.FloatField()

class ThematicObjectiveSerializer(serializers.Serializer):
    description = serializers.CharField()
    amount = serializers.FloatField()

class Top10ThematicObjectivesSerializer(serializers.ListField):
    def __init__(self, *args, **kwargs):
        kwargs["child"] = ThematicObjectiveSerializer()
        super().__init__(*args, **kwargs)

class ProjectTypologySerializer(serializers.Serializer):
    type = serializers.CharField()
    amount = serializers.FloatField()

class Top10ProjectTypologiesSerializer(serializers.ListField):
    def __init__(self, *args, **kwargs):
        kwargs["child"] = ProjectTypologySerializer()
        super().__init__(*args, **kwargs)

class FundsToBeFoundSerializer(serializers.Serializer):
    number_of_projects_with_gap = serializers.IntegerField()
    total_missing_amount = serializers.FloatField()

class PaymentsRealizationGapSerializer(serializers.Serializer):
    total_realized_cost = serializers.FloatField()
    total_payments_made = serializers.FloatField()
    overall_difference = serializers.FloatField()

# -----------------------------
# Financing Analysis (MAIN BLOCK)
# -----------------------------

class AnalysisSerializer(serializers.Serializer):
    filters = AnalysisFiltersSerializer()
    funding_sources_analysis = FundingSourcesAnalysisSerializer()
    specific_funds_contribution = SpecificFundsContributionSerializer()
    top10_thematic_objectives = Top10ThematicObjectivesSerializer()
    top10_project_typologies = Top10ProjectTypologiesSerializer()
    funds_to_be_found = FundsToBeFoundSerializer()
    payments_realization_gap = PaymentsRealizationGapSerializer()

