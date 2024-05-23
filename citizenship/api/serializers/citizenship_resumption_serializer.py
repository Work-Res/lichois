from rest_framework import serializers
from lichois.citizenship.models import CitizenshipResumption


class CitizenshipResumptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CitizenshipResumption
        fields = '__all__'
