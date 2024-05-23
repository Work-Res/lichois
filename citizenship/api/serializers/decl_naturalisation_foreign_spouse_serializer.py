from rest_framework import serializers
from lichois.citizenship.models import DeclarationNaturalisationByForeignSpouse


class DeclNaturalisationForeignSpouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeclarationNaturalisationByForeignSpouse
        fields = '__all__'
