import logging

from ..api.dto import SecurityClearanceRequestDTO
from ..api.serializers import SecurityClearanceSerializer
from ..models import SecurityClearance
from app.api.common.web import APIMessage, APIResponse

from django.db import transaction


class SecurityClearanceService:

    def __init__(self, security_clearance_request: SecurityClearanceRequestDTO, user=None):
        self.security_clearance_request = security_clearance_request
        self.user = user
        self.logger = logging.getLogger(__name__)
        self.response = APIResponse()

    @transaction.atomic()
    def create_clearance(self):
        security_clearance = SecurityClearance.objects.create(
            status=self.security_clearance_request.status,
            summary=self.security_clearance_request.summary,
            document_number=self.security_clearance_request.document_number,
            approved_by=self.user
        )
        api_message = APIMessage(
            code=200,
            message="Security clearance created successfully.",
            details=f"Security clearance created successfully."
        )
        self.response.status = "success"
        self.response.data = SecurityClearanceSerializer(security_clearance).data
        self.response.messages.append(api_message.to_dict())
