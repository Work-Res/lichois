from rest_framework import serializers
from ..models import Naturalisation


class NaturalisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Naturalisation
        fields = '__all__'
