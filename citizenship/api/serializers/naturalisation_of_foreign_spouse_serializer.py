from rest_framework import serializers
from lichois.citizenship.models import NaturalisationOfForeignSpouse


class NaturalisationOfForeignSpouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = NaturalisationOfForeignSpouse
        fields = '__all__'
