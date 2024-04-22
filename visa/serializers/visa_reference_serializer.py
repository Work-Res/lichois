from rest_framework import serializers
from ..models import VisaReference


class VisaReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisaReference
        fields = '__all__'
