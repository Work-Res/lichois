from rest_framework import serializers
from citizenship.models import WitnessDetails


class WitnessDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WitnessDetails
        fields = '__all__'
