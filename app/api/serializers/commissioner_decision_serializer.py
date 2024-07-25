from rest_framework import serializers

from app_decision.api.serializers import ApplicationDecisionTypeSerializer
from ...models import CommissionerDecision

from ...validators import CommissionerDecisionValidator


class CommissionerDecisionSerializer(serializers.ModelSerializer):

    status = ApplicationDecisionTypeSerializer()

    def validate(self, data):
        validator = CommissionerDecisionValidator(
            document_number=data.get("document_number")
        )
        if not validator.is_valid():
            raise serializers.ValidationError(validator.response.messages)

    class Meta:
        model = CommissionerDecision
        fields = "__all__"
