from app.models.security_clearance import SecurityClearance
from ..api.dto import RecommendationRequestDTO
from ..api.serializers import CommissionerDecisionSerializer, DirectorDecisionSerializer
from ..models import CommissionerDecision, DirectorDecision
from ..service import BaseDecisionService
from ..utils.system_enums import ApplicationStatusEnum
from ..workflow.transaction_data import RecommendationTransitionData


class RecommendationService(BaseDecisionService):
    def __init__(self, recommendation_request: RecommendationRequestDTO):

        workflow = RecommendationTransitionData()
        workflow.recommendation_decision = recommendation_request.status.upper()
        workflow.status = recommendation_request.status.upper()

        super().__init__(
            request=recommendation_request,
            application_field_key="recommendation",
            workflow=workflow,
            task_to_deactivate=ApplicationStatusEnum.RECOMMENDATION.value,
        )

    def create_commissioner_recommendation(self):
        return self.create_decision(
            CommissionerDecision, CommissionerDecisionSerializer
        )

    def retrieve_commissioner_recommendation(self):
        return self.retrieve_decision(
            CommissionerDecision, CommissionerDecisionSerializer
        )
    
    def create_director_recommendation(self):
        return self.create_decision(
            DirectorDecision, DirectorDecisionSerializer
        )

    def retrieve_director_recommendation(self):
        return self.retrieve_decision(
            DirectorDecision, DirectorDecisionSerializer
        )




class RecommendationServiceOverideVetting(RecommendationService):

    def _has_security_clearance(self):
        return False
