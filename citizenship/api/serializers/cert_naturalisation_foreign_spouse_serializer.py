from rest_framework import serializers
from lichois.citizenship.models import CertNaturalisationByForeignSpouse


class CertNaturalisationByForeignSpouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CertNaturalisationByForeignSpouse
        fields = '__all__'
