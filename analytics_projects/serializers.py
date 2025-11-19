from rest_framework import serializers

class SectorSerializer(serializers.Serializer):
    name = serializers.CharField()
    total_financing = serializers.FloatField()

class OverviewSerializer(serializers.Serializer):
    top_sectors = serializers.DictField(child=SectorSerializer())
