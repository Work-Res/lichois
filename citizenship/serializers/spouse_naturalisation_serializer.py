from rest_framework import serializers
from ..models import SpouseNaturalization


class SpouseNaturalizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpouseNaturalization
        fields = '__all__'
