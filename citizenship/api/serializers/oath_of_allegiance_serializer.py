from rest_framework import serializers
from lichois.citizenship.models import OathOfAllegiance


class OathOfAllegianceSerializer(serializers.ModelSerializer):
    class Meta:
        model = OathOfAllegiance
        fields = '__all__'
