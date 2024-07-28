from django.db import transaction

import app
from app.utils.system_enums import ApplicationStatusEnum
from app.workflow.transaction_data import (
    MinisterDecisionTransactionData,
    ProductionTransactionData,
    RecommendationTransitionData,
)

from ..api.dto import MinisterRequestDTO
from ..api.serializers import MinisterDecisionSerializer
from ..models import MinisterDecision
from ..service import BaseDecisionService


class MinisterDecisionService(BaseDecisionService):
    def __init__(self, decision_request: MinisterRequestDTO):
        workflow = ProductionTransactionData(
            recommendation_decision=decision_request.status.upper()
        )
        super().__init__(
            request=decision_request,
            workflow=workflow,
            task_to_deactivate=ApplicationStatusEnum.RECOMMENDATION.value,
            application_field_key="recommendation",
        )

    def create_minister_decision(self):
        return self.create_decision(MinisterDecision, MinisterDecisionSerializer)

    def retrieve_minister_decision(self):
        return self.retrieve_decision(MinisterDecision, MinisterDecisionSerializer)
