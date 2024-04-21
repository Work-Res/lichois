from rest_framework import serializers
from ...models import ExemptionCertificate


class ExemptionCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExemptionCertificate
        fields = '__all__'
        