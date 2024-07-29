from rest_framework import serializers
from citizenship.models import PlaceOfResidence


class PlaceOfResidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceOfResidence
        fields = '__all__'
