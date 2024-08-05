import os
from rest_framework import serializers

from ...models.assessment import Assessment
from ...validators.assessment_validator import AssessmentValidator
from app_checklist.utils.read_json import ReadJSON


class AssessmentSerializer(serializers.ModelSerializer):

    document_number = serializers.CharField(required=True)

    def validate(self, data):

        file_name = "marking_score_work_and_residence.json"
        file_location = os.path.join(
            os.getcwd(), "app_assessment", "data", "assessments", file_name
        )
        reader = ReadJSON(file_location=file_location)

        assessment = Assessment(**data)
        validator = AssessmentValidator(assessment=assessment, rules=reader.json_data())
        if not validator.is_valid():
            raise serializers.ValidationError(validator.response.result())

        return data

    class Meta:
        model = Assessment
        fields = "__all__"
