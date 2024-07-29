from rest_framework import serializers
from citizenship.models import TravelCertNonCitizen


class TravelCertNonCitizenSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelCertNonCitizen
        fields = '__all__'
