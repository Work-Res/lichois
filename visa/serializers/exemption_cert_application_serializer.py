from rest_framework import serializers
from lichois.visa.models import ExemptionCertificateApplication


class ExemptionCertificateApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExemptionCertificateApplication
        fields = '__all__'
