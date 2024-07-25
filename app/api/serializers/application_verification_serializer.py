from rest_framework import serializers
from app_decision.api.serializers import ApplicationDecisionTypeSerializer

from ...models import ApplicationVerification


class ApplicationVerificationSerializer(serializers.ModelSerializer):
    status = ApplicationDecisionTypeSerializer()
    summary = serializers.CharField(max_length=200, required=False, allow_blank=True)

    class Meta:
        model = ApplicationVerification
        fields = "__all__"
