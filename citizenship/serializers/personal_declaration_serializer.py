from rest_framework import serializers
from ..models import PersonalDeclaration


class PersonalDeclarationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalDeclaration
        fields = '__all__'