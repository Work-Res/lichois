import os

from rest_framework import serializers

from app_assessment.models.appeal_assessment import AppealAssessment
from app_assessment.models.assessement_case_decision import AssessmentCaseDecision
from app_assessment.models.assessment import Assessment
from app_assessment.models.assessment_case_note import AssessmentCaseNote
from app_assessment.models.assessment_case_summary import AssessmentCaseSummary
from app_assessment.models.assessment_emergency import AssessmentEmergency
from app_assessment.models.dependant_assessment import DependantAssessment
from app_checklist.utils import ReadJSON
from ..models import AssessmentResult, NewAssessmentInvestor, RenewalAssessmentInvestor
from app_assessment.validators import AssessmentValidator


class AssessmentResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentResult
        fields = ["id", "score", "output_results", "result_date"]


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


class NewAssessmentInvestorSerializer(serializers.ModelSerializer):

    document_number = serializers.CharField(required=True)

    def validate(self, data):

        file_name = "marking_score_work_and_residence_new_investor.json"
        file_location = os.path.join(
            os.getcwd(), "app_assessment", "data", "assessments", file_name
        )
        reader = ReadJSON(file_location=file_location)

        assessment = NewAssessmentInvestor(**data)
        validator = AssessmentValidator(assessment=assessment, rules=reader.json_data())
        if not validator.is_valid():
            raise serializers.ValidationError(validator.response.result())

        return data

    class Meta:
        model = NewAssessmentInvestor
        fields = "__all__"


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


class AssessmentEmergencySerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentEmergency
        fields = "__all__"


class AppealAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppealAssessment
        fields = "__all__"


class DependantAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DependantAssessment
        fields = "__all__"
