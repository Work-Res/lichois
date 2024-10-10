from app.service import BaseDecisionService
from app.utils.system_enums import ApplicationStatusEnum
from app.workflow import MinisterDecisionTransactionData, PresidentDecisionTransactionData

from citizenship.api.dto.citizenship_minister_decision_request_dto import (
    CitizenshipMinisterDecisionSerializer, CitizenshipPresidentDecisionSerializer,
)
from citizenship.api.dto.request_dto import CitizenshipMinisterRequestDTO
from citizenship.models import CitizenshipMinisterDecision, CitizenshipPresidentDecision

from citizenship.classes.mixins.update_section10b_mixin import UpdateSection10bMixin


class CitizenshipPresidentDecisionService(BaseDecisionService, UpdateSection10bMixin):
    def __init__(self, decision_request: CitizenshipMinisterRequestDTO):
        self.decision_request = decision_request
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
        decision = self.create_decision(
            CitizenshipPresidentDecision, CitizenshipPresidentDecisionSerializer
        )
        self.update_field(self.decision_request.document_number,
                          field_key="president_decision", field_value=self.decision_request.status.upper())

        return decision


    def retrieve_president_decision(self):
        return self.retrieve_decision(
            CitizenshipPresidentDecision, CitizenshipPresidentDecisionSerializer
        )

    def _security_clearance(self):
        return None
