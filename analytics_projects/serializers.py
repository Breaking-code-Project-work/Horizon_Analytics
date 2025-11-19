from rest_framework import serializers

class FiltersOverviewSerializer(serializers.Serializer):
    region = serializers.CharField()
    macroarea = serializers.CharField()

class ProjectSerializer(serializers.Serializer):
    id = serializers.CharField()
    Title = serializers.CharField()
    TotalFinancing = serializers.FloatField()
    Region = serializers.CharField()
    Macroarea = serializers.CharField()

class TopProjectsSerializer(serializers.DictField):
    child = ProjectSerializer()

class SectorSerializer(serializers.Serializer):
    Name = serializers.CharField()
    Totalfinancing = serializers.FloatField()

class TopSectorsSerializer(serializers.DictField):
    child = SectorSerializer()

class OverviewSerializer(serializers.Serializer):
    Filters = FiltersOverviewSerializer()
    numberOfProjects = serializers.IntegerField()
    totalFinancing = serializers.FloatField()
    numberEndedProjects = serializers.IntegerField()
    numberNotStartedProjects = serializers.IntegerField()
    numberProjectsInProgress = serializers.IntegerField()
    MiddayFinancing = serializers.FloatField()
    MiddleNorthFinancing = serializers.FloatField()
    TopProjects = TopProjectsSerializer()
    numberBigProjects = serializers.IntegerField()
    TopSectors = TopSectorsSerializer()