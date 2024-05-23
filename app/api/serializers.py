from django.contrib.auth.models import User


from rest_framework import serializers
# from rest_framework.fields import CharField
# https://docs.viewflow.io/workflow/quick_start.html


from app.models import (Application, ApplicationStatus, ApplicationDocument, ApplicationVersion, ApplicationUser)


class ApplicationStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApplicationStatus
        fields = (
            'id',
            'code',
            'name',
            'processes',
            'valid_from',
            'valid_to',
        )


class ApplicationUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApplicationUser
        fields = (
            'id', 'full_name', 'user_identifier', 'work_location_code', 'dob')


class ApplicationDocumentSerializer(serializers.ModelSerializer):

    applicant = ApplicationUserSerializer()

    class Meta:
        model = ApplicationDocument
        fields = (
            'id',
            'document_number',
            'document_date',
            'signed_date',
            'applicant',
            'submission_customer',
        )


class ApplicationSerializer(serializers.ModelSerializer):

    application_status = ApplicationStatusSerializer()
    application_document = ApplicationDocumentSerializer()

    class Meta:
        model = Application
        fields = (
            'id',
            'last_application_version_id',
            'application_type',
            'application_status',
            'application_document',
        )


class ApplicationVersionSerializer(serializers.ModelSerializer):

    application = ApplicationSerializer()

    class Meta:
        model = ApplicationVersion
        fields = (
            'application',
            'version_number'
        )


class NewApplicationSerializer(serializers.Serializer):

    process_name = serializers.CharField(max_length=200, required=True)
    full_name = serializers.CharField(max_length=200, required=True)
    applicant_identifier = serializers.CharField(allow_blank=False, max_length=200, required=True)
    work_place = serializers.CharField(allow_blank=False, max_length=200, required=True)
    status = serializers.CharField(max_length=30)
    dob = serializers.CharField(max_length=30)


class ApplicationVerificationRequestSerializer(serializers.Serializer):

    decision = serializers.CharField(max_length=200, required=True)
    comment = serializers.CharField(max_length=500, required=True)
    outcome_reason = serializers.CharField(max_length=300, required=False)