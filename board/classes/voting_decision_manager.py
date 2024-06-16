import logging

from workresidentpermit.models import SecurityClearance
from ..choices import ACCEPTED, REJECTED, APPROVED
from ..models import BoardDecision, BoardMeeting, BoardMeetingVote


class VotingDecisionManager(object):
	
	def __init__(self, document_number, board_meeting):
		self.document_number = document_number
		self._security_clearance = None
		self._board_decision = None
		self.board_meeting = board_meeting
		self.logger = logging.getLogger(__name__)
	
	def _create_voting_decision(self):
		total_approved = self.get_approved_votes()
		total_rejected = self.get_rejected_votes()
		
		if total_approved == 0 and total_rejected == 0:
			print("Total approved and rejected votes are 0")
			self.logger.error(f"No votes have been cast for {self.document_number}")
		elif total_approved == total_rejected:
			print("Total approved and rejected votes are equal")
			self.logger.info(f"Chairperson has to break the tie, no board decision")
			raise Exception("Chairperson has to break the tie, no board decision")
		elif total_approved > total_rejected:
			print("Total rejected votes are less than total approved votes")
			return ACCEPTED
		elif total_approved < total_rejected:
			print("Total rejected votes are more than total approved votes")
			return REJECTED
		return None
	
	def get_approved_votes(self):
		approved_votes = BoardMeetingVote.objects.filter(status=APPROVED, document_number=self.document_number).count()
		return approved_votes
	
	def get_rejected_votes(self):
		rejected_votes = BoardMeetingVote.objects.filter(status=REJECTED, document_number=self.document_number).count()
		return rejected_votes
	
	def security_clearance(self):
		if not self._security_clearance:
			try:
				return SecurityClearance.objects.get(
					document_number=self.document_number
				)
			except SecurityClearance.DoesNotExist:
				print(f"Security clearance is pending for {self.document_number}")
				self.logger.info(f"Security clearance is pending for {self.document_number}")
		else:
			return self._security_clearance
	
	def create_board_decision(self):
		try:
			self._board_decision = BoardDecision.objects.get(
				assessed_application__application_document__document_number=self.document_number
			)
			print("Board decision already exists")
		except BoardDecision.DoesNotExist:
			voting_decision_outcome = self._create_voting_decision()
			print("Voting decision outcome: ", voting_decision_outcome)
			security_clearance = self.security_clearance()
			print("Security clearance status: ", security_clearance.status.code.lower())
			if voting_decision_outcome:
				print("Voting outcome: ", voting_decision_outcome)
				self._board_decision = BoardDecision.objects.create(
					assessed_application__application_document__document_number=self.document_number,
					decision_outcome=voting_decision_outcome,
					board_meeting=self.board_meeting,
					vetting_outcome=security_clearance.status.code.lower()
				)
		finally:
			return self._board_decision
