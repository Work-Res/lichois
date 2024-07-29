import os
from rest_framework import serializers

from ...models.renewal_assessment_investor import RenewalAssessmentInvestor
from ...validators.assessment_validator import AssessmentValidator
from app_checklist.utils.read_json import ReadJSON


class RenewalAssessmentInvestorSerializer(serializers.ModelSerializer):

    document_number = serializers.CharField(required=True)

    def validate(self, data):

        file_name = "marking_score_work_and_residence_renewal_investor.json"
        file_location = os.path.join(
            os.getcwd(), "app_assessment", "data", "assessments", file_name
        )
        reader = ReadJSON(file_location=file_location)

        assessment = RenewalAssessmentInvestor(**data)
        validator = AssessmentValidator(assessment=assessment, rules=reader.json_data())
        if not validator.is_valid():
            raise serializers.ValidationError(validator.response.result())
        return data

    class Meta:
        model = RenewalAssessmentInvestor
        fields = "__all__"
