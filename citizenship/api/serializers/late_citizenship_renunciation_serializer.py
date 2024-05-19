from rest_framework import serializers
from lichois.citizenship.models import LateCitizenshipRenunciation


class LateCitizenshipRenunciationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LateCitizenshipRenunciation
        fields = '__all__'
