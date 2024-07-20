from django.contrib.auth.models import User

from rest_framework import serializers

# from rest_framework.fields import CharField
# https://docs.viewflow.io/workflow/quick_start.html


from app.models import (
    Application,
    ApplicationStatus,
    ApplicationDocument,
    ApplicationVersion,
    ApplicationUser,
    ApplicationVerification,
    ApplicationRenewalHistory,
)
from board.models import BoardDecision
from workresidentpermit.models import SecurityClearance
from app_decision.api.serializers import ApplicationDecisionTypeSerializer
from app_comments.api.serializers import CommentSerializer


class ApplicationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationStatus
        fields = (
            "id",
            "code",
            "name",
            "processes",
            "valid_from",
            "valid_to",
        )


class ApplicationUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationUser
        fields = ("id", "full_name", "user_identifier", "work_location_code", "dob")


class ApplicationDocumentSerializer(serializers.ModelSerializer):
    applicant = ApplicationUserSerializer()

    class Meta:
        model = ApplicationDocument
        fields = (
            "id",
            "document_number",
            "document_date",
            "signed_date",
            "applicant",
            "applicant_type",
            "submission_customer",
        )


class ApplicationSerializer(serializers.ModelSerializer):
    application_status = ApplicationStatusSerializer()
    application_document = ApplicationDocumentSerializer()

    class Meta:
        model = Application
        fields = (
            "id",
            "last_application_version_id",
            "application_type",
            "application_status",
            "application_document",
            "batched",
            "board",
            "security_clearance",
            "verification",
            "permit_period",
        )


class ApplicationVersionSerializer(serializers.ModelSerializer):
    application = ApplicationSerializer()

    class Meta:
        model = ApplicationVersion
        fields = ("application", "version_number")


class NewApplicationSerializer(serializers.Serializer):
    process_name = serializers.CharField(max_length=200, required=True)
    full_name = serializers.CharField(max_length=200, required=True)
    applicant_identifier = serializers.CharField(
        allow_blank=False, max_length=200, required=True
    )
    work_place = serializers.CharField(allow_blank=False, max_length=200, required=True)
    status = serializers.CharField(max_length=30)
    dob = serializers.CharField(max_length=30)


class RenewalApplicationSerializer(serializers.Serializer):
    process_name = serializers.CharField(max_length=200, required=True)
    applicant_identifier = serializers.CharField(
        allow_blank=False, max_length=200, required=True
    )
    document_number = serializers.CharField(max_length=200, required=True)
    work_place = serializers.CharField(allow_blank=False, max_length=200, required=True)


class ApplicationVerificationSerializer(serializers.ModelSerializer):
    decision = ApplicationDecisionTypeSerializer()
    outcome_reason = serializers.CharField(
        max_length=200, required=False, allow_blank=True
    )

    class Meta:
        model = ApplicationVerification
        fields = ("document_number", "decision", "outcome_reason", "comment")


class ApplicationVerificationRequestSerializer(serializers.Serializer):
    decision = serializers.CharField(max_length=200, required=True)
    comment = serializers.CharField(max_length=500, required=False, allow_blank=True)
    outcome_reason = serializers.CharField(
        max_length=300, required=False, allow_blank=True
    )


class ApplicationRenewalDTOSerializer(serializers.Serializer):
    proces_name = serializers.CharField(max_length=200, required=False)
    applicant_identifier = serializers.CharField(max_length=200, required=True)
    document_number = serializers.CharField(max_length=200, required=True)


class ApplicationRenewalHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ApplicationRenewalHistory
        fields = ("application_type", "comment", "process_name", "historical_record")
