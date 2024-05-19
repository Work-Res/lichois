from rest_framework import serializers
from lichois.citizenship.models import CitizenshipRenunciationDeclaration


class CitizenshipRenunciationDeclarationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CitizenshipRenunciationDeclaration
        fields = '__all__'
