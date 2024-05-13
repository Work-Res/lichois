from rest_framework import serializers
from ..models import ResidentialHistory


class ResidentialHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ResidentialHistory
        fields = '__all__'
