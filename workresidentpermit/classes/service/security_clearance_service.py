from django.db import transaction

from workresidentpermit.api.dto import SecurityClearanceRequestDTO
from workresidentpermit.api.serializers import SecurityClearanceSerializer
from workresidentpermit.classes.service.base_decision_service import BaseDecisionService
from workresidentpermit.models import SecurityClearance


class SecurityClearanceService(BaseDecisionService):
	def __init__(self, security_clearance_request: SecurityClearanceRequestDTO, user=None):
		super().__init__(security_clearance_request, user)
	
	@transaction.atomic
	def create_clearance(self):
		return self.create_decision(SecurityClearance, SecurityClearanceSerializer)
