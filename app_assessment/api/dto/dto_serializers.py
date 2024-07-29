from rest_framework import serializers

from app_assessment.models.choices import DECISION_TYPE


class AssessmentNoteRequestDTOSerializer(serializers.Serializer):
    document_number = serializers.CharField(max_length=100, required=True)
    parent_object_id = serializers.CharField(max_length=200, required=True)
    parent_object_type = serializers.CharField(max_length=200, required=True)
    note_text = serializers.CharField(max_length=2000, required=True)
    note_type = serializers.CharField(max_length=100, required=True)


class AssessmentCaseDecisionDTOSerializer(serializers.Serializer):
    document_number = serializers.CharField(max_length=100, required=True)
    parent_object_id = serializers.CharField(max_length=200, required=True)
    parent_object_type = serializers.CharField(max_length=200, required=True)
    author = serializers.CharField(max_length=150, required=True)
    author_role = serializers.CharField(max_length=200, required=True)
    decision = serializers.ChoiceField(choices=DECISION_TYPE, required=True)


class CaseSummaryRequestDTOSerializer(serializers.Serializer):
    parent_object_id = serializers.CharField(max_length=200, required=False)
    parent_object_type = serializers.CharField(max_length=200, required=False)
    data = serializers.JSONField(required=False)
    summary = serializers.CharField(max_length=200, required=True)
    document_number = serializers.CharField(max_length=100, required=True)
