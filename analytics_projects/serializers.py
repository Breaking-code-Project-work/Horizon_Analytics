from rest_framework import serializers

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

class ProjectTypologySerializer(serializers.Serializer):
    typology = serializers.CharField()
    amount = serializers.FloatField()
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
    top_project_typologies = ProjectTypologySerializer(many=True)


