from rest_framework import serializers

class SectorFundingSerializer(serializers.Serializer):
    name = serializers.CharField()
    total_financing = serializers.FloatField()
