from rest_framework import serializers
from ..models import RenunciationOfForeignCitizenship


class RenunciationOfForeignCitizenshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = RenunciationOfForeignCitizenship
        fields = '__all__'
