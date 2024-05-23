from rest_framework import serializers
from lichois.citizenship.models import WitnessDetails


class WitnessDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WitnessDetails
        fields = '__all__'
