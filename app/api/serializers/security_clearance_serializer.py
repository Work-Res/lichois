from rest_framework import serializers

from .application_decision_type_serializer import ApplicationDecisionTypeSerializer

from ...models import SecurityClearance


class SecurityClearanceSerializer(serializers.ModelSerializer):

    status = ApplicationDecisionTypeSerializer()

    class Meta:
        model = SecurityClearance
        fields = "__all__"
