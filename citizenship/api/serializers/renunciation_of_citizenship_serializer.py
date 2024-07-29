from rest_framework import serializers
from citizenship.models import RenunciationOfCitizenship


class RenunciationOfCitizenshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = RenunciationOfCitizenship
        fields = '__all__'
