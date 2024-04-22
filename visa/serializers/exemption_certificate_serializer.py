from rest_framework import serializers
from ..models import ExemptionCertificate


class VisaExemptionCertSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExemptionCertificate
        fields = '__all__'
