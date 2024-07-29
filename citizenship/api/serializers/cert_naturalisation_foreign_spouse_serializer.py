from rest_framework import serializers
from citizenship.models import CertNaturalisationByForeignSpouse


class CertNaturalisationByForeignSpouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CertNaturalisationByForeignSpouse
        fields = '__all__'
