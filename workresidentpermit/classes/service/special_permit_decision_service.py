import logging

from app.models import Application

from app_comments.models import Comment
from workresidentpermit.models import CommissionerDecision, MinisterDecision
from app.utils import ApplicationDecisionEnum

from workresidentpermit.workflow import ProductionTransactionData

from .application_decision_service import ApplicationDecisionService


class SpecialPermitDecisionService(ApplicationDecisionService):
	""" Responsible for create application decision based on commissioner's decision.
    """
	
	def __init__(self, document_number, commissioner_decision: CommissionerDecision = None,
	             comment: Comment = None, minister_decision: MinisterDecision = None):
		self.document_number = document_number
		self.comment = comment
		super().__init__(document_number=document_number, comment=comment)
		self._commissioner_decision = commissioner_decision
		self._minister_decision = minister_decision
		self.application = Application.objects.get(application_document__document_number=document_number)
		self.workflow = ProductionTransactionData()
		self.logger = logging.getLogger(__name__)
	
	def minister_decision(self):
		if not self._minister_decision:
			try:
				self._minister_decision = MinisterDecision.objects.get(
					document_number=self.document_number
				)
			except MinisterDecision.DoesNotExist:
				pass
		else:
			return self._minister_decision
	
	def commissioner_decision(self):
		if not self._commissioner_decision:
			try:
				self._commissioner_decision = CommissionerDecision.objects.get(
					document_number=self.document_number
				)
			except CommissionerDecision.DoesNotExist:
				pass
		else:
			return self._commissioner_decision
	
	def decision_predicate(self):
		is_commissioner_decision = False
		is_minister_decision = False
		
		commissioner_decision = self.commissioner_decision()
		if commissioner_decision:
			is_commissioner_decision = commissioner_decision.status.code.lower() == \
			                           ApplicationDecisionEnum.ACCEPTED.value.lower()
		
		minister_decision = self.minister_decision()
		if minister_decision:
			is_minister_decision = minister_decision.status.code.lower() == \
			                       ApplicationDecisionEnum.ACCEPTED.value.lower()
		
		if is_commissioner_decision:
			self.decision_value = ApplicationDecisionEnum.ACCEPTED.value
			self.workflow.commissioner_decision = ApplicationDecisionEnum.ACCEPTED.value
			return True
		elif commissioner_decision:
			self.decision_value = ApplicationDecisionEnum.REJECTED.value
			self.workflow.commissioner_decision = ApplicationDecisionEnum.REJECTED.value
			return True
		elif is_minister_decision:
			self.decision_value = ApplicationDecisionEnum.ACCEPTED.value
			self.workflow.minister_decision = ApplicationDecisionEnum.ACCEPTED.value
		else:
			self.logger.info("Application decision cannot be completed, pending security clearance or board decision.")
			return False
	
	def commissioner_approval_process(self):
		pass
	
	def minister_approval_process(self):
		pass
