from app.models.application_verification import ApplicationVerification
from app.service import BaseDecisionService
from app.utils.system_enums import ApplicationStatusEnum
from app.workflow.transaction_data import OfficerTransactionData

from ..api.dto import ApplicationVerificationRequestDTO
from ..api.serializers import ApplicationVerificationSerializer


class VerificationService(BaseDecisionService):

    def __init__(self, verification_request: ApplicationVerificationRequestDTO):
        workflow = OfficerTransactionData(
            verification_decision=verification_request.status
        )

        super().__init__(
            request=verification_request,
            application_field_key="verification",
            workflow=workflow,
            task_to_deactivate=ApplicationStatusEnum.VERIFICATION.value,
        )

    def create_verification(self):
        return self.create_decision(
            ApplicationVerification, ApplicationVerificationSerializer
        )

    def retrieve_verification(self):
        return self.retrieve_decision(
            ApplicationVerification, ApplicationVerificationSerializer
        )
