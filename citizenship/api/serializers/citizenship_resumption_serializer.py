from rest_framework import serializers
from citizenship.models import CitizenshipResumption


class CitizenshipResumptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CitizenshipResumption
        fields = '__all__'
