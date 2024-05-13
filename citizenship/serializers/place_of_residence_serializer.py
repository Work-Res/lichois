from rest_framework import serializers
from ..models import PlaceOfResidence


class PlaceOfResidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceOfResidence
        fields = '__all__'
