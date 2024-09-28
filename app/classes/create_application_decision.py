import logging

from ..models import ApplicationDecisionType


class CreateApplicationDecision:
    """Based on the board decision the system should create application decision."""

    def __init__(self, board_decision):
        self.board_decision = board_decision
        self.decision_type = self.board_decision.decision_outcome

    def create(self):
        pass

    def application_decision(self):
        try:
            return ApplicationDecisionType.objects.get(code=self.decision_type)
        except ApplicationDecisionType.DoesNotExist:
            pass
