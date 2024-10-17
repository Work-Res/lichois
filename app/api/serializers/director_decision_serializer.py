from rest_framework import serializers

from .application_decision_type_serializer import ApplicationDecisionTypeSerializer
from ...models import DirectorDecision

from ...validators import DecisionValidator


class DirectorDecisionSerializer(serializers.ModelSerializer):

    status = ApplicationDecisionTypeSerializer()

    def validate(self, data):
        validator = DecisionValidator(document_number=data.get("document_number"))
        if not validator.is_valid():
            raise serializers.ValidationError(validator.response.messages)

    class Meta:
        model = DirectorDecision
        fields = "__all__"
