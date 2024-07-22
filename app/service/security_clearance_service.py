from django.db import transaction

from workresidentpermit.classes.service.base_decision_service import BaseDecisionService

from ..api.dto import SecurityClearanceRequestDTO
from ..api.serializers import SecurityClearanceSerializer
from ..models import SecurityClearance


class SecurityClearanceService(BaseDecisionService):
    def __init__(
        self, security_clearance_request: SecurityClearanceRequestDTO, user=None
    ):
        super().__init__(security_clearance_request, user)

    def create_clearance(self):
        self.create_decision(SecurityClearance, SecurityClearanceSerializer)
        self.update_application()
