from rest_framework import serializers
from citizenship.models import NationalityDeclaration


class NationalityDeclarationSerializer(serializers.ModelSerializer):
    class Meta:
        model = NationalityDeclaration
        fields = '__all__'
