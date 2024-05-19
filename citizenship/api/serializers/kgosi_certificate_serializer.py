from rest_framework import serializers
from lichois.citizenship.models import KgosiCertificate


class KgosiCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = KgosiCertificate
        fields = '__all__'
