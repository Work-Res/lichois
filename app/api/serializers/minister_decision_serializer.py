from rest_framework import serializers

from ...models import MinisterDecision


class MinisterDecisionRequestDTOSerializer(serializers.Serializer):
    document_number = serializers.CharField(max_length=200, required=True)
    status = serializers.CharField(max_length=200, required=True)
    summary = serializers.CharField(max_length=500, required=False, allow_blank=True)


class MinisterDecisionSerializer(serializers.Serializer):
    class Meta:
        model = MinisterDecision
        fields = (
            "document_number",
            "date_requested",
            "date_approved",
            "status",
            "summary",
        )
