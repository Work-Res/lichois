from rest_framework import serializers
from ...models import AssessmentCaseNote


class AssessmentCaseNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentCaseNote
        fields = "__all__"
