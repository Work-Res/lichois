
from app.service import BaseDecisionService
from app.utils.system_enums import ApplicationStatusEnum
from app.workflow.transaction_data import (
    RecommendationDecisionTransactionData,
)
from citizenship.api.dto import RecommendationDecisionRequestDTO

from citizenship.api.serializers import RecommendationDecisionSerializer
from citizenship.models import RecommendationDecision


class RecommendationDecisionService(BaseDecisionService):
    def __init__(self, decision_request: RecommendationDecisionRequestDTO):
        workflow = RecommendationDecisionTransactionData(
            recommendation_decision=decision_request.status.upper()
        )
        super().__init__(
            request=decision_request,
            workflow=workflow,
            task_to_deactivate=ApplicationStatusEnum.RECOMMENDATION.value,
            application_field_key="recommendation",
        )

    def create_recommendation(self):
        return self.create_decision(RecommendationDecision, RecommendationDecisionSerializer)

    def retrieve_recommendation(self):
        return self.retrieve_decision(RecommendationDecision, RecommendationDecisionSerializer)

    def _security_clearance(self):
        return None
