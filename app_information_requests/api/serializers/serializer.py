from rest_framework import serializers

from app_information_requests.models import InformationRequest
from app_information_requests.models.missing_details import InformationMissingRequest


class InformationMissingRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = InformationMissingRequest
        fields = ['id', 'information_request', 'parent_object_id', 'parent_type', 'reason', 'description',
                  'is_provided']


class InformationRequestSerializer(serializers.ModelSerializer):
    missing_requests = InformationMissingRequestSerializer(many=True, read_only=True)

    class Meta:
        model = InformationRequest
        fields = ['id', 'resolution', 'submitter', 'process_name', 'application_type', 'office_location',
                  'missing_requests']
