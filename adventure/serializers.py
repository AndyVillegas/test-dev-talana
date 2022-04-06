from rest_framework import serializers


class JourneySerializer(serializers.Serializer):
    name = serializers.CharField()
    passengers = serializers.IntegerField()


class EmptyJourneySerializer(serializers.Serializer):
    pass
