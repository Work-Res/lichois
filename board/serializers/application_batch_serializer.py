from rest_framework import serializers

from app.api.serializers import ApplicationSerializer
from ..models import ApplicationBatch


class ApplicationBatchSerializer(serializers.ModelSerializer):
    applications = ApplicationSerializer(many=True)

    def validate(self, attrs):
        return attrs

    class Meta:
        model = ApplicationBatch
        fields = "__all__"
