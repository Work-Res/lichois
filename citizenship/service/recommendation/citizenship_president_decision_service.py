from app.service import BaseDecisionService
from app.utils.system_enums import ApplicationStatusEnum
from app.workflow import MinisterDecisionTransactionData, PresidentDecisionTransactionData

from citizenship.api.dto.citizenship_minister_decision_request_dto import (
    CitizenshipMinisterDecisionSerializer, CitizenshipPresidentDecisionSerializer,
)
from citizenship.api.dto.request_dto import CitizenshipMinisterRequestDTO
from citizenship.models import CitizenshipMinisterDecision, CitizenshipPresidentDecision


class CitizenshipPresidentDecisionService(BaseDecisionService):
    def __init__(self, decision_request: CitizenshipMinisterRequestDTO):
        president_decision = (
            decision_request.status.upper() if decision_request.status else ""
        )
        workflow = PresidentDecisionTransactionData(president_decision=president_decision)
        super().__init__(
            request=decision_request,
            workflow=workflow,
            task_to_deactivate=ApplicationStatusEnum.MINISTER_DECISION.value,
            application_field_key="recommendation",
        )

    def create_president_decision(self):
        return self.create_decision(
            CitizenshipPresidentDecision, CitizenshipPresidentDecisionSerializer
        )

    def retrieve_president_decision(self):
        return self.retrieve_decision(
            CitizenshipPresidentDecision, CitizenshipPresidentDecisionSerializer
        )

    def _security_clearance(self):
        return None
