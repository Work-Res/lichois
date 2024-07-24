from rest_framework import serializers

from ...models import ApplicationRenewalHistory


class ApplicationRenewalHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ApplicationRenewalHistory
        fields = ("application_type", "comment", "process_name", "historical_record")


class RenewalApplicationSerializer(serializers.Serializer):
    process_name = serializers.CharField(max_length=200, required=True)
    applicant_identifier = serializers.CharField(
        allow_blank=False, max_length=200, required=True
    )
    document_number = serializers.CharField(max_length=200, required=True)
    work_place = serializers.CharField(allow_blank=False, max_length=200, required=True)
