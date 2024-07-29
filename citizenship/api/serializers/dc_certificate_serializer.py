from rest_framework import serializers
from citizenship.models import DCCertificate


class DCCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DCCertificate
        fields = '__all__'
