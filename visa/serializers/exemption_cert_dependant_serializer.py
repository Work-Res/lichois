from rest_framework import serializers
from ..models import ExemptionCertificateDependant


class ExemptionCertificateDependantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExemptionCertificateDependant
        fields = '__all__'
