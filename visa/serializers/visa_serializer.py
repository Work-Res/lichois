from rest_framework import serializers
from lichois.visa.models import Visa


class VisaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visa
        fields = '__all__'
