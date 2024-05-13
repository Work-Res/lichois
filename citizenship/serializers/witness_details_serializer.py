from rest_framework import serializers
from ..models import WitnessDetails


class WitnessDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WitnessDetails
        fields = '__all__'
