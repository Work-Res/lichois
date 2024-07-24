from rest_framework import serializers


class NewApplicationSerializer(serializers.Serializer):
    process_name = serializers.CharField(max_length=200, required=True)
    application_type = serializers.CharField(max_length=200, required=False)
    full_name = serializers.CharField(max_length=200, required=True)
    applicant_identifier = serializers.CharField(
        allow_blank=False,
        max_length=200,
        required=True,
    )
    work_place = serializers.CharField(allow_blank=False, max_length=200, required=True)
    status = serializers.CharField(max_length=30)
    dob = serializers.CharField(max_length=30)
    applicant_type = serializers.CharField(max_length=200, required=False)
