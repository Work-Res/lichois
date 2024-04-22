from rest_framework import serializers
from app_personal_details.api.serializers import PersonSerializer, PassportSerializer
from app_address.api.serializers import ApplicationAddressSerializer
from .permit_serializer import PermitSerializer
from .child_serializer import ChildSerializer
from .spouse_serializer import SpouseSerializer
from .work_residence_permit_serializer import WorkResidencePermitSerializer


class WorkResidentPermitDataSerializer(serializers.Serializer):
    personal_details = PersonSerializer()
    address = ApplicationAddressSerializer()
    passport = PassportSerializer()
    permit = PermitSerializer()
    child = ChildSerializer(many=True)
    spouse = SpouseSerializer(many=True)
    form_details = WorkResidencePermitSerializer()
