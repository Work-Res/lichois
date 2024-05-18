from rest_framework.exceptions import PermissionDenied

from board.models import BoardMeetingVote, BoardMember


class BoardMeetingVoteManager:
	def __init__(self, user):
		self.user = user
	
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
		voted_approved_members = BoardMeetingVote.objects.filter(status='approved').values_list(
			'meeting_attendee__board_member__user', flat=True)
		# Get
		voted_rejected_members = BoardMeetingVote.objects.filter(status='rejected').values_list(
			'meeting_attendee__board_member__user', flat=True)
		# Get the board members who have not voted
		not_voted_members = board_members.exclude(id__in=voted_approved_members).exclude(
			id__in=voted_rejected_members)
		# Return the voted approved members, voted rejected members, and not voted members
		return {
			'voted_approved_members': voted_approved_members,
			'voted_rejected_members': voted_rejected_members,
			'not_voted_members': not_voted_members,
		}
