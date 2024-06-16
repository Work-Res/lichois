from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from app.api.common.web import APIMessage
from ..choices import APPROVED, PRESENT
from ..models import BoardMeeting, BoardMember, MeetingAttendee, MeetingInvitation
from ..serializers import BoardMeetingSerializer


class BoardMeetingViewSet(viewsets.ModelViewSet):
	queryset = BoardMeeting.objects.all().order_by('meeting_date')
	serializer_class = BoardMeetingSerializer
	
	def get_queryset(self):
		"""
		Optionally restricts the returned meetings to a given board,
		by filtering against a `board` query parameter in the URL.
		"""
		board_member = BoardMember.objects.filter(user=self.request.user).first()
		if not board_member:
			api_message = APIMessage(
				code=403,
				message="Bad request",
				details="User is not a member of any board"
			)
			raise PermissionDenied(api_message.to_dict())
			
		queryset = BoardMeeting.objects.filter(board=board_member.board)
		return queryset
	
	@action(detail=False, methods=['get'], url_path='accepted', url_name='accepted')
	def get_accepted_meeting(self, request):
		# Retrieve the board member or raise a 404 error if not found
		try:
			# Attempt to retrieve the board member
			board_member = get_object_or_404(BoardMember, user=request.user)
		except Http404:
			# Create a custom APIMessage and raise PermissionDenied if not found
			api_message = APIMessage(
				code=400,
				message="Bad request",
				details="User is not a member of any board"
			)
			raise PermissionDenied(detail=api_message.to_dict())
		else:
			# Filter and order BoardMeeting objects using the related MeetingAttendee objects
			meetings = BoardMeeting.objects.filter(
				meetingattendee__board_member=board_member,
				meetingattendee__attendance_status=PRESENT  # Adjust the status value as necessary
			).order_by('meeting_date')
			
			# Serialize the filtered and ordered meetings
			serialized_meetings = BoardMeetingSerializer(meetings, many=True)
			
			return Response(data=serialized_meetings.data)

	
	
