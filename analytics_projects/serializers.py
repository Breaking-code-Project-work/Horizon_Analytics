from rest_framework import serializers

class OverviewSerializer(serializers.Serializer):
    TopSectors = serializers.ListField()

