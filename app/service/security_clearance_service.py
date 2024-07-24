from django.db import transaction

from app.models.application import Application
from app.workflow.transaction_data import VettingTransactionData
from workflow.signals import create_or_update_task_signal

from ..api.dto import SecurityClearanceRequestDTO
from ..api.serializers import SecurityClearanceSerializer
from ..models import SecurityClearance
from ..service import BaseDecisionService


class SecurityClearanceService(BaseDecisionService):
    def __init__(
        self,
        security_clearance_request: SecurityClearanceRequestDTO,
        user=None,
        document_number: str = None,
    ):
        super().__init__(security_clearance_request, user)
        self.application = Application.objects.get(
            application_document__document_number=document_number
        )

    @transaction.atomic
    def create_clearance(self):
        self.create_decision(SecurityClearance, SecurityClearanceSerializer)
        self.update_application()
        self.update_workflow()

    def update_workflow(self):
        workflow = VettingTransactionData()
        if self.decision:
            workflow.verification_decision = self.decision.code.upper()
            workflow.vetting_obj_exists = True
            create_or_update_task_signal.send(
                self.application,
                source=workflow,
                application=self.application,
            )
