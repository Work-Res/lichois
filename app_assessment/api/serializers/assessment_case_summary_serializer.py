from rest_framework import serializers
from ...models import AssessmentCaseSummary


class AssessmentCaseSummarySerializer(serializers.ModelSerializer):
    document_number = serializers.CharField(required=True)
    data = serializers.JSONField(required=False)

    class Meta:
        model = AssessmentCaseSummary
        fields = "__all__"
