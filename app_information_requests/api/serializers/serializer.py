import os

from rest_framework import serializers

from app_information_requests.models import InformationRequest
from app_information_requests.models.missing_details import InformationMissingRequest
from app_information_requests.service import InformationRequestService


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

    def create(self, validated_data):
        template_path = os.path.join(
            "app_information_requests", "data",  "templates", "information_request_template.docx")
        missing_requests_data = validated_data.pop('missing_requests')
        service = InformationRequestService(
            template_path=template_path
        )
        info_request = service.create_information_request(
            submitter_id=validated_data['submitter'].id,
            process_name=validated_data['process_name'],
            application_type=validated_data['application_type'],
            office_location=validated_data['office_location'],
            due_date=validated_data['due_date'],
            missing_requests_data=missing_requests_data
        )
        return info_request
