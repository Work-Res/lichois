from rest_framework import serializers
from citizenship.models import CitizenshipSummary


class CitizenshipSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = CitizenshipSummary
        fields = '__all__'
