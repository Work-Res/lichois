from rest_framework import status, viewsets
from rest_framework.response import Response

from app.api.common.web import APIMessage
from ..models import BoardMeeting, BoardMember
from ..serializers import BoardMeetingSerializer


class BoardMeetingViewSet(viewsets.ModelViewSet):
	queryset = BoardMeeting.objects.all()
	serializer_class = BoardMeetingSerializer
	
	def create(self, request, *args, **kwargs):
		auth_user = request.user
		board = BoardMember.objects.filter(user=auth_user).first().board
		if not board:
			api_message = APIMessage(
				code=400,
				message="Bad request",
				details="User is not a member of any board"
			)
			return Response(data=api_message.to_dict(), status=status.HTTP_400_BAD_REQUEST)
		data = request.data.copy()  # Make a mutable copy
		data['board'] = board.id  # Modify the copy
		request._data = data  # Assign the modified copy back to request.data
		return super().create(request, *args, **kwargs)
	
	
