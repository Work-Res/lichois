from rest_framework import serializers
from citizenship.models import RenunciationOfForeignCitizenship


class RenunciationOfForeignCitizenshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = RenunciationOfForeignCitizenship
        fields = '__all__'
