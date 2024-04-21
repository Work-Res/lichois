from rest_framework import serializers
from ..models import InterestDeclaration


class InterestDeclarationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterestDeclaration
        fields = '__all__'
