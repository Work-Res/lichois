from rest_framework import serializers
from ..models import BlueCardApplication


class BlueCardApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlueCardApplication
        fields = '__all__'
