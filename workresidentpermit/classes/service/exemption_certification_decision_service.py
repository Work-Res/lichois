import logging

from django.db import transaction

from app.models import Application

from app_comments.models import Comment
from workresidentpermit.models import SecurityClearance

from workresidentpermit.workflow import RecommendationTransitionData

from .application_decision_service import ApplicationDecisionService
from ...exceptions import ApplicationRequiredDecisionException, WorkflowRequiredDecisionException


class ExemptionCertificateDecisionService(ApplicationDecisionService):
	""" Responsible for creation of commissioner recommendation exemption certificate decision. """
	
	def __init__(self, document_number, security_clearance: SecurityClearance = None,
	             comment: Comment = None):
		self.document_number = document_number
		self.comment = comment
		super().__init__(document_number=document_number, comment=comment)
		self._security_clearance = security_clearance
		self._verification = None
		self.application = Application.objects.get(application_document__document_number=document_number)
		self.workflow = RecommendationTransitionData()
		self.logger = logging.getLogger(__name__)
	
	def decision_predicate(self):
		if self._security_clearance:
			# if self._security_clearance.status.code.lower() == ApplicationDecisionEnum.ACCEPTED.value.lower():
			# 	self.workflow.security_clearance = ApplicationDecisionEnum.ACCEPTED.value.upper()
			return True
		return False
	
	@transaction.atomic()
	def create_application_decision(self):
		if not self.application:
			raise ApplicationRequiredDecisionException()
		if not self.workflow:
			raise WorkflowRequiredDecisionException()
		if self.decision_predicate():
			self.run_workflow(application=self.application, workflow=self.workflow)

			
