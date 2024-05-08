from rest_framework import serializers
from ..models import OathOfAllegiance


class OathOfAllegianceSerializer(serializers.ModelSerializer):
    class Meta:
        model = OathOfAllegiance
        fields = '__all__'
