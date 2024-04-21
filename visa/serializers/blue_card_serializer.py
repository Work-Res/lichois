from rest_framework import serializers
from lichois.visa.models import BlueCard


class BlueCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlueCard
        fields = '__all__'
