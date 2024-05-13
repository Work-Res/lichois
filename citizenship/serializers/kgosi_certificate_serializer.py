from rest_framework import serializers
from ..models import KgosiCertificate


class KgosiCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = KgosiCertificate
        fields = '__all__'
