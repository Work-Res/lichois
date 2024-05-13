from rest_framework import serializers
from ..models import DCCertificate


class DCCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DCCertificate
        fields = '__all__'
