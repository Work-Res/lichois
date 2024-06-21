from django.db.models import Q
from rest_framework.exceptions import PermissionDenied

from board.models import BoardMeetingVote, BoardMember, InterestDeclaration, MeetingAttendee


class BoardMeetingVoteManager:
	def __init__(self, user, document_number):
		self.user = user
		self.document_number = document_number
	
	def get_votes(self):
		board_member = BoardMember.objects.filter(user=self.user).first()
		# Check if user is a member of any board
		if not board_member:
			raise PermissionDenied("User is not a member of any board")
		# Get the board of the user
		board = board_member.board
		# Get the board members
		board_members = BoardMember.objects.filter(board=board)
		# Get the board meeting votes of the board members and filter them by status (approved or rejected)
		voted_approved_members = BoardMeetingVote.objects.filter(Q(status='approved') & Q(
			document_number=self.document_number)).values_list(
			'meeting_attendee__board_member__user__username', flat=True)
		# Get
		voted_rejected_members = BoardMeetingVote.objects.filter(Q(status='rejected') & Q(
			document_number=self.document_number)).values_list(
			'meeting_attendee__board_member__user__username', flat=True)
		# Get the list of members who have voted
		voted = BoardMeetingVote.objects.filter(
			document_number=self.document_number).values_list('meeting_attendee__board_member__id', flat=True)
		# Get the board members who have not voted
		not_voted_members = board_members.exclude(id__in=voted).values_list('user__username', flat=True)
		# Return the voted approved members, voted rejected members, and not voted members
		return {
			'voted_approved_members': list(voted_approved_members),
			'voted_rejected_members': list(voted_rejected_members),
			'not_voted_members': list(not_voted_members),
		}
	
	def create_tie_breaker(self, tie_breaker):
		try:
			declaration = InterestDeclaration.objects.get(Q(meeting_attendee__board_member__user=self.user) & Q(
				document_number=self.document_number) & Q(decision='vote'))
		except MeetingAttendee.DoesNotExist:
			pass
		else:
			if self.user.is_chairperson:
				meeting_attendee = declaration.meeting_attendee
				try:
					vote = BoardMeetingVote.objects.get(Q(meeting_attendee=meeting_attendee) & Q(
						document_number=self.document_number))
				except BoardMeetingVote.DoesNotExist:
					raise PermissionDenied('User is not a board member')
				else:
					vote.tie_breaker = tie_breaker
					vote.save()
					return tie_breaker
			raise PermissionDenied('User is not chairperson')
	
	def vote_exists(self):
		try:
			declaration = InterestDeclaration.objects.get(Q(meeting_attendee__board_member__user=self.user) & Q(
				document_number=self.document_number) & Q(decision='vote'))
		except InterestDeclaration.DoesNotExist:
			pass
		else:
			meeting_attendee = declaration.meeting_attendee
			try:
				BoardMeetingVote.objects.get(Q(meeting_attendee=meeting_attendee) & Q(
					document_number=self.document_number))
			except BoardMeetingVote.DoesNotExist:
				return False
			return True
		return False
	
	# get vote of current user logged in
	def get_my_vote(self):
		try:
			# Get the meeting attendee of the user
			declaration = InterestDeclaration.objects.get(Q(meeting_attendee__board_member__user=self.user) & Q(
				document_number=self.document_number) & Q(decision='vote'))
		except InterestDeclaration.DoesNotExist:
			pass
		else:
			meeting_attendee = declaration.meeting_attendee
			try:
				vote = BoardMeetingVote.objects.get(Q(meeting_attendee=meeting_attendee) & Q(
					document_number=self.document_number))
			except BoardMeetingVote.DoesNotExist:
				return None
			return vote
		return None

