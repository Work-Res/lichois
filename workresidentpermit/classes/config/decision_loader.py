from app.utils import ApplicationDecisionEnum
from workresidentpermit.models import CommissionerDecision, MinisterDecision, SecurityClearance
from app.models import ApplicationVerification
import logging

# Configure the root logger
logging.basicConfig(level=logging.WARNING)

log = logging.getLogger(__name__)


class DecisionLoader:
	""" Retrieve decision objects. """
	
	def __init__(self, document_number):
		self.document_number = document_number
		self.decisions = {
			CommissionerDecision: None,
			MinisterDecision: None,
			ApplicationVerification: None,
			SecurityClearance: None,
		}
	
	def get_decision(self, decision_class) -> object:
		""" Retrieve the decision object based on the class type. """
		if self.decisions[decision_class] is None:
			try:
				decision = decision_class.objects.get(document_number=self.document_number)
				self.decisions[decision_class] = decision
			except decision_class.DoesNotExist:
				log.warning(f"{decision_class.__name__} not found for document number {self.document_number}")
				return None
		return self.decisions[decision_class]
	
	def is_decision_accepted(self, decision_class):
		""" Check if a decision of a given class is accepted. """
		decision = self.get_decision(decision_class)
		return decision and decision.status.code.lower() == ApplicationDecisionEnum.ACCEPTED.value.lower()
