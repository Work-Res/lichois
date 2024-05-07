from rest_framework import serializers
from ..models import NaturalisationOfForeignSpouse


class NaturalisationOfForeignSpouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = NaturalisationOfForeignSpouse
        fields = '__all__'
