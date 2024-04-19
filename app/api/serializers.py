from django.contrib.auth.models import User


from rest_framework import serializers
# from rest_framework.fields import CharField
# https://docs.viewflow.io/workflow/quick_start.html


from app.models import (Application, ApplicationStatus, ApplicationDocument, ApplicationVersion, ApplicationUser)


class ApplicationStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApplicationStatus
        fields = (
            'code',
            'name',
            'processes',
            'valid_from',
            'valid_to',
        )


class ApplicationUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApplicationUser
        fields = ('user_identifier', 'work_location_code')


class ApplicationDocumentSerializer(serializers.ModelSerializer):

    applicant = ApplicationUser()

    class Meta:
        model = ApplicationDocument
        fields = (
            'document_number',
            'document_date',
            'signed_date',
            'submission_customer',
        )


class ApplicationSerializer(serializers.ModelSerializer):

    application_status = ApplicationStatusSerializer()
    application_document = ApplicationDocumentSerializer()

    class Meta:
        model = Application
        fields = (
            'last_application_version_id',
            'application_status',
            'application_document',
        )


class ApplicationVersionSerializer(serializers.ModelSerializer):

    application = ApplicationSerializer()

    class Meta:
        model = ApplicationVersion
        fields = (
            'application',
            'version_number',
            'comment',
        )


class NewApplicationSerializer(serializers.Serializer):

    proces_name = serializers.CharField(max_length=200, required=True)
    applicant_identifier = serializers.CharField(allow_blank=False, max_length=200, required=True)
    work_place = serializers.CharField(allow_blank=False, max_length=200, required=True)
    status = serializers.CharField(max_length=30)
    dob = serializers.CharField(max_length=30)

    def validate_applicant_identifier(self, value):
        """
        Check if the applicant exists before open new application.
        """
        exits = ApplicationUser.objects.exists(user_identifier=value)
        if exits:
            raise serializers.ValidationError(f"Applicant with {value} identifier does not exists.")
        return value

    def validate(self, data):
        """
        Check if there is open application for this application.
        """
        application_identifier = data.get("applicant_identifier")
        status = data.get("applicant_identifier")
        exits = Application.objects.exists(
            application_status__status=status,
            application_document__applicant__user_identifier=application_identifier)
        if exits:
            raise serializers.ValidationError(
                f"An application with (NEW) status exists for applicant: {application_identifier}, complete the "
                f"existing before open new application")
        return data
