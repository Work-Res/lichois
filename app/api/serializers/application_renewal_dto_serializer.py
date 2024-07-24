from rest_framework import serializers


class ApplicationRenewalDTOSerializer(serializers.Serializer):
    proces_name = serializers.CharField(max_length=200, required=False)
    applicant_identifier = serializers.CharField(max_length=200, required=True)
    document_number = serializers.CharField(max_length=200, required=True)
