from rest_framework import serializers

from app_decision.api.serializers import ApplicationDecisionTypeSerializer

from ...models import SecurityClearance


class SecurityClearanceSerializer(serializers.ModelSerializer):

    status = ApplicationDecisionTypeSerializer()

    class Meta:
        model = SecurityClearance
        fields = "__all__"