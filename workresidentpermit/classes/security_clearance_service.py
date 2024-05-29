import logging

from datetime import datetime

from app_decision.models import ApplicationDecisionType
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

    def get_application_decision_type(self):
        try:
            application_decision_type =ApplicationDecisionType.objects.get(
                code__iexact=self.security_clearance_request.status
            )
        except ApplicationDecisionType.DoesNotExist:
            pass
        else:
            return application_decision_type

    @transaction.atomic()
    def create_clearance(self):
        security_clearance = SecurityClearance.objects.create(
            status=self.get_application_decision_type(),
            summary=self.security_clearance_request.summary,
            document_number=self.security_clearance_request.document_number,
            approved_by=self.user,
            date_approved=datetime.now()
        )
        api_message = APIMessage(
            code=200,
            message="Security clearance created successfully.",
            details=f"Security clearance created successfully."
        )
        self.response.status = "success"
        self.response.data = SecurityClearanceSerializer(security_clearance).data
        self.response.messages.append(api_message.to_dict())
