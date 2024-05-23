from rest_framework import serializers
from ..models import DeclarationNaturalisationByForeignSpouse


class DeclNaturalisationForeignSpouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeclarationNaturalisationByForeignSpouse
        fields = '__all__'