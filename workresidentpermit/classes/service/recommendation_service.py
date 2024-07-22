from django.db import transaction
from workresidentpermit.api.dto import RecommendationRequestDTO
from workresidentpermit.api.serializers import CommissionerDecisionSerializer
from app.service import BaseDecisionService
from workresidentpermit.models import CommissionerDecision


class RecommendationService(BaseDecisionService):
    def __init__(self, recommendation_request: RecommendationRequestDTO, user=None):
        super().__init__(recommendation_request, user)

    def create_recommendation(self):
        return self.create_decision(
            CommissionerDecision, CommissionerDecisionSerializer
        )

    def retrieve_recommendation(self):
        return self.retrieve_decision(
            CommissionerDecision, CommissionerDecisionSerializer
        )
