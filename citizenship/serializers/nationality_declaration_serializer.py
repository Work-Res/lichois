from rest_framework import serializers
from ..models import NationalityDeclaration


class NationalityDeclarationSerializer(serializers.ModelSerializer):
    class Meta:
        model = NationalityDeclaration
        fields = '__all__'
