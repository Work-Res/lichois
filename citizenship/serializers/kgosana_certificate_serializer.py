from rest_framework import serializers
from ..models import KgosanaCertificate


class KgosanaCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = KgosanaCertificate
        fields = '__all__'
