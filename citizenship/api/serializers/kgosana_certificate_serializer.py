from rest_framework import serializers
from citizenship.models import KgosanaCertificate


class KgosanaCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = KgosanaCertificate
        fields = '__all__'
