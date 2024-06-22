from django.db import transaction

from workresidentpermit.api.dto import MinisterRequestDTO
from workresidentpermit.api.serializers import MinisterDecisionSerializer
from workresidentpermit.classes.service.base_decision_service import BaseDecisionService
from workresidentpermit.models import MinisterDecision


class MinisterDecisionService(BaseDecisionService):
	def __init__(self, decision_request: MinisterRequestDTO, user=None):
		super().__init__(decision_request, user)
	
	def create_minister_decision(self):
		return self.create_decision(MinisterDecision, MinisterDecisionSerializer)
	
	def retrieve_minister_decision(self):
		return self.retrieve_decision(MinisterDecision, MinisterDecisionSerializer)