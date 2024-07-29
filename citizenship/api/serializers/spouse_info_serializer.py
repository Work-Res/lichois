from rest_framework import serializers
from citizenship.models import SpouseInfo


class SpouseInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpouseInfo
        fields = '__all__'
