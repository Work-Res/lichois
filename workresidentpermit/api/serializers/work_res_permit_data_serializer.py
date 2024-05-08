from rest_framework import serializers
from app_personal_details.api.serializers import PersonSerializer, PassportSerializer
from app_address.api.serializers import ApplicationAddressSerializer
from app_attachments.api.serializers import ApplicationAttachmentSerializer
from app_contact.api.serializers import ApplicationContactSerializer
from .permit_serializer import PermitSerializer
from .child_serializer import ChildSerializer
from .spouse_serializer import SpouseSerializer
from .residence_permit_serializer import ResidencePermitSerializer


class WorkResidentPermitDataSerializer(serializers.Serializer):
    personal_details = PersonSerializer()
    address = ApplicationAddressSerializer()
    contacts = ApplicationContactSerializer()
    passport = PassportSerializer()
    permit = PermitSerializer()
    child = ChildSerializer(many=True)
    spouse = SpouseSerializer(many=True)
    attachments = ApplicationAttachmentSerializer(many=True)
    resident_permit = ResidencePermitSerializer()
