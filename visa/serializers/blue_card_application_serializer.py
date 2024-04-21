from rest_framework import serializers
from lichois.visa.models import BlueCardApplication


class BlueCardApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlueCardApplication
        fields = '__all__'
