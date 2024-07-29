from rest_framework import serializers
from citizenship.models import Naturalisation


class NaturalisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Naturalisation
        fields = '__all__'
