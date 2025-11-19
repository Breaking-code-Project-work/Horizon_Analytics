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
    child = ProjectSerializer()

class SectorSerializer(serializers.Serializer):
    name = serializers.CharField()
    total_financing = serializers.FloatField()

class TopSectorsSerializer(serializers.DictField):
    child = SectorSerializer()

class OverviewSerializer(serializers.Serializer):
    filters = FiltersOverviewSerializer()
    numberOfProjects = serializers.IntegerField()
    totalFinancing = serializers.FloatField()
    numberEndedProjects = serializers.IntegerField()
    numberNotStartedProjects = serializers.IntegerField()
    numberProjectsInProgress = serializers.IntegerField()
    middayFinancing = serializers.FloatField()
    middleNorthFinancing = serializers.FloatField()
    nationalFinancing = serializers.FloatField()
    abroadFinancing = serializers.FloatField()
    trasversalFinancing = serializers.FloatField()
    top_projects = TopProjectsSerializer()
    numberBigProjects = serializers.IntegerField()
    topSectors = TopSectorsSerializer()