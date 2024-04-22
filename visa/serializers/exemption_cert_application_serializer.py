from rest_framework import serializers
from ..models import ExemptionCertificateApplication


class VisaExemptionCertificateAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExemptionCertificateApplication
        fields = '__all__'
