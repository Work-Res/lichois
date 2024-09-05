from rest_framework import serializers

from app_assessment.models.choices import DECISION_TYPE


class AssessmentNoteRequestDTOSerializer(serializers.Serializer):
    document_number = serializers.CharField(max_length=100, required=True)
    parent_object_id = serializers.CharField(max_length=200, required=False)
    parent_object_type = serializers.CharField(max_length=200, required=False)
    note_text = serializers.CharField(max_length=2000, required=False)
    note_type = serializers.CharField(max_length=100, required=False)
    decision = serializers.ChoiceField(choices=DECISION_TYPE, required=False)
    status = serializers.CharField(max_length=150, required=False)
    summary = serializers.CharField(max_length=150, required=False)


class AssessmentCaseDecisionDTOSerializer(serializers.Serializer):
    document_number = serializers.CharField(max_length=100, required=True)
    parent_object_id = serializers.CharField(max_length=200, required=False)
    parent_object_type = serializers.CharField(max_length=200, required=False)
    author = serializers.CharField(max_length=150, required=False)
    author_role = serializers.CharField(max_length=200, required=False)
    decision = serializers.ChoiceField(choices=DECISION_TYPE, required=False)
    status = serializers.CharField(max_length=150, required=False)
    summary = serializers.CharField(max_length=150, required=False)


class CaseSummaryRequestDTOSerializer(serializers.Serializer):
    parent_object_id = serializers.CharField(max_length=200, required=False)
    parent_object_type = serializers.CharField(max_length=200, required=False)
    data = serializers.JSONField(required=False)
    summary = serializers.CharField(max_length=200, required=True)
    document_number = serializers.CharField(max_length=100, required=True)
