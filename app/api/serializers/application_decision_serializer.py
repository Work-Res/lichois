from rest_framework import serializers

from ...models import ApplicationDecision
from .application_decision_type_serializer import ApplicationDecisionTypeSerializer


class ApplicationDecisionSerializer(serializers.ModelSerializer):

    final_decision_type = ApplicationDecisionTypeSerializer()

    proposed_decision_type = ApplicationDecisionTypeSerializer()

    class Meta:
        model = ApplicationDecision
        fields = (
            "document_number",
            "final_decision_type",
            "proposed_decision_type",
            "created",
            "modified",
            # 'application_document'
        )
