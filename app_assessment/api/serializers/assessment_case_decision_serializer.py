from rest_framework import serializers
from ...models import AssessmentCaseDecision


class AssessmentCaseDecisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentCaseDecision
        fields = "__all__"
