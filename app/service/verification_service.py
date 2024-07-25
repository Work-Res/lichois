from app.api.dto.serializers import ApplicationVerificationRequestDTOSerializer
from app.models.application_verification import ApplicationVerification
from app.service import BaseDecisionService
from app.utils.system_enums import ApplicationStatusEnum
from app.workflow.transaction_data import OfficerTransactionData
from app_decision.models.application_decision_type import ApplicationDecisionType

from ..api.dto import ApplicationVerificationRequestDTO
from ..api.serializers import ApplicationVerificationSerializer


class VerificationService(BaseDecisionService):

    def __init__(self, verification_request: ApplicationVerificationRequestDTO):
        workflow = OfficerTransactionData(
            verification_decision=self._get_application_decision_type(
                verification_request
            ).code,
        )

        super().__init__(
            request=verification_request,
            application_field_key="verification",
            workflow=workflow,
            task_to_deactivate=ApplicationStatusEnum.VERIFICATION.value,
        )

    def create_verification(self):
        return self.create_decision(
            ApplicationVerification, ApplicationVerificationRequestDTOSerializer
        )

    def retrieve_verification(self):
        return self.retrieve_decision(
            ApplicationVerification, ApplicationVerificationSerializer
        )

    def _get_application_decision_type(self, verification_request):
        return ApplicationDecisionType.objects.get(
            code__iexact=verification_request.status.lower()
        )
