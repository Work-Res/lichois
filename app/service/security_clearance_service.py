from django.db import transaction

from ..api.dto import SecurityClearanceRequestDTO
from ..api.serializers import SecurityClearanceSerializer
from ..models import SecurityClearance
from ..service import BaseDecisionService
from ..utils.system_enums import ApplicationStatusEnum
from ..workflow.transaction_data import VettingTransactionData


class SecurityClearanceService(BaseDecisionService):
    def __init__(self, security_clearance_request: SecurityClearanceRequestDTO):
        workflow = VettingTransactionData(
            vetting_decision=security_clearance_request.status.upper(),
            vetting_obj_exists=True,
        )

        super().__init__(
            request=security_clearance_request,
            application_field_key="security_clearance",
            task_to_deactivate=ApplicationStatusEnum.VETTING.value,
            workflow=workflow,
        )

    @transaction.atomic
    def create_clearance(self):
        return self.create_decision(SecurityClearance, SecurityClearanceSerializer)
