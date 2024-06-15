class VerificationTransactionData:
	
	def __init__(self, next_activity_name=None, application_status=None, system_verification=None):
		self.next_activity_name = next_activity_name
		self.current_status = application_status
		self.system_verification = system_verification


class VettingTransactionData:
	
	def __init__(self, next_activity_name=None, verification_decision=None, current_status=None):
		self.current_status = current_status
		self.next_activity_name = next_activity_name
		self.verification_decision = verification_decision


class RecommendationTransitionData:
	def __init__(self, next_activity_name=None, application_status=None, verification_decision=None):
		self.next_activity_name = next_activity_name
		self.application_status = application_status
		self.verification_decision = verification_decision


class ProductionTransactionData:
	
	def __init__(self, previous_status=None, board_decision=None, security_clearance=None, current_status=None,
	             next_activity_name=None):
		self.previous_status = previous_status
		self.board_decision = board_decision
		self.security_clearance = security_clearance
		self.current_status = current_status
		self.next_activity_name = next_activity_name
