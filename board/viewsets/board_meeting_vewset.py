from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from app.api.common.web import APIMessage
from ..choices import APPROVED
from ..models import BoardMeeting, BoardMember, MeetingInvitation
from ..serializers import BoardMeetingSerializer


class BoardMeetingViewSet(viewsets.ModelViewSet):
	queryset = BoardMeeting.objects.all()
	serializer_class = BoardMeetingSerializer
	
	def get_queryset(self):
		"""
		Optionally restricts the returned meetings to a given board,
		by filtering against a `board` query parameter in the URL.
		"""
		board_member = BoardMember.objects.filter(user=self.request.user).first()
		if not board_member:
			api_message = APIMessage(
				code=400,
				message="Bad request",
				details="User is not a member of any board"
			)
			raise PermissionDenied(api_message.to_dict())
			
		queryset = BoardMeeting.objects.filter(board=board_member.board)
		return queryset
	
	@action(detail=False, methods=['get'], url_path='accepted',
	        url_name='accepted')
	def get_accepted_meeting(self, request):
		board_member = BoardMember.objects.filter(user=self.request.user).first()
		if not board_member:
			api_message = APIMessage(
				code=400,
				message="Bad request",
				details="User is not a member of any board"
			)
			raise PermissionDenied(api_message.to_dict())
		meetings = []
		meeting_invitations = MeetingInvitation.objects.filter(
			invited_user=board_member,
			status=APPROVED)
		for invitation in meeting_invitations:
			meetings.append(invitation.board_meeting)
		return Response(data=BoardMeetingSerializer(meetings, many=True).data)
	
	
