from rest_framework import serializers
from lichois.citizenship.models import SpouseInfo


class SpouseInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpouseInfo
        fields = '__all__'
