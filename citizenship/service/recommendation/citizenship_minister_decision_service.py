from app.service import BaseDecisionService
from app.utils.system_enums import ApplicationStatusEnum
from app.workflow import MinisterDecisionTransactionData

from citizenship.api.dto.citizenship_minister_decision_request_dto import CitizenshipMinisterDecisionSerializer
from citizenship.api.dto.request_dto import CitizenshipMinisterRequestDTO
from citizenship.models import CitizenshipMinisterDecision


class CitizenshipMinisterDecisionService(BaseDecisionService):
    def __init__(self, decision_request: CitizenshipMinisterRequestDTO):
        workflow = MinisterDecisionTransactionData(
            minister_decision=decision_request.status.upper()
        )
        super().__init__(
            request=decision_request,
            workflow=workflow,
            task_to_deactivate=ApplicationStatusEnum.MINISTER_DECISION.value,
            application_field_key="recommendation",
        )

    def create_minister_decision(self):
        return self.create_decision(CitizenshipMinisterDecision, CitizenshipMinisterDecisionSerializer)

    def retrieve_minister_decision(self):
        return self.retrieve_decision(CitizenshipMinisterDecision, CitizenshipMinisterDecisionSerializer)

    def _security_clearance(self):
        return None
