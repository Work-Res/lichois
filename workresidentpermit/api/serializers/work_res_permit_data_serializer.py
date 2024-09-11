from rest_framework import serializers

from app.api.serializers import (
    ApplicationSerializer,
    ApplicationVerificationSerializer,
    SecurityClearanceSerializer,
)
from app_address.api.serializers import ApplicationAddressSerializer
from app_attachments.api.serializers import ApplicationAttachmentSerializer
from app_contact.api.serializers import ApplicationContactSerializer
from app_personal_details.api.serializers import (
    PassportSerializer,
    PermitSerializer,
    PersonSerializer,
    ChildSerializer,
    SpouseSerializer,
)
from board.serializers import BoardDecisionSerializer

from .residence_permit_serializer import ResidencePermitSerializer
from .work_permit_serializer import WorkPermitSerializer


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
    work_permit = WorkPermitSerializer()
    application = ApplicationSerializer()
    application_verification = ApplicationVerificationSerializer()
    security_clearance = SecurityClearanceSerializer()
    board_decision = BoardDecisionSerializer()
