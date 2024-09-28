from rest_framework import serializers
from app.models import ApplicationDecisionType


class ApplicationDecisionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationDecisionType
        fields = ("code", "name", "process_types", "valid_from", "valid_to")
