from rest_framework import serializers
from ..models import TravelCertificatePermit


class TravelCertificatePermitSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelCertificatePermit
        fields = '__all__'
