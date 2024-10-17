from app.service import BaseDecisionService
from app.utils.system_enums import ApplicationStatusEnum
from app.workflow import ForeignRenunciationDecisionTransactionData

from citizenship.api.dto.citizenship_minister_decision_request_dto import (
    ForeignRenunciationDecisionSerializer,
)
from citizenship.api.dto import ForeignRenunciationRequestDTO
from citizenship.models import ForeignRenunciationDecision


class ForeignRenunciationDecisionService(BaseDecisionService):
    def __init__(self, decision_request: ForeignRenunciationRequestDTO):
        renunciation_decision = (
            decision_request.status.upper() if decision_request.status else ""
        )
        workflow = ForeignRenunciationDecisionTransactionData(renunciation_decision=renunciation_decision)
        super().__init__(
            request=decision_request,
            workflow=workflow,
            task_to_deactivate=ApplicationStatusEnum.MINISTER_DECISION.value,
            application_field_key="recommendation",
        )

    def create_foreign_renunciation_decision(self):
        return self.create_decision(
            ForeignRenunciationDecision, ForeignRenunciationDecisionSerializer
        )

    def retrieve_foreign_renunciation_decision(self):
        return self.retrieve_decision(
            ForeignRenunciationDecision, ForeignRenunciationDecisionSerializer
        )
