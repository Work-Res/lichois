from django.db import transaction

import app

from ..api.dto import MinisterRequestDTO
from ..api.serializers import MinisterDecisionSerializer
from ..models import MinisterDecision
from ..service import BaseDecisionService


class MinisterDecisionService(BaseDecisionService):
    def __init__(self, decision_request: MinisterRequestDTO, user=None):
        super().__init__(decision_request, user, application_field="minister_decision")

    def create_minister_decision(self):
        return self.create_decision(MinisterDecision, MinisterDecisionSerializer)

    def retrieve_minister_decision(self):
        return self.retrieve_decision(MinisterDecision, MinisterDecisionSerializer)
