from rest_framework import serializers
from ..models import Under20Citizenship


class Under20CitizenshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Under20Citizenship
        fields = '__all__'
