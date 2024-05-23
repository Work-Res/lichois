from rest_framework import serializers
from lichois.citizenship.models import ResidentialHistory


class ResidentialHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ResidentialHistory
        fields = '__all__'
