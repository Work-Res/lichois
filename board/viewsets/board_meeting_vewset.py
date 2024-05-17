from rest_framework import status, viewsets
from rest_framework.response import Response

from app.api.common.web import APIMessage
from ..models import BoardMeeting, BoardMember
from ..serializers import BoardMeetingSerializer


class BoardMeetingViewSet(viewsets.ModelViewSet):
	queryset = BoardMeeting.objects.all()
	serializer_class = BoardMeetingSerializer


def create(self, request, *args, **kwargs):
	board = BoardMember.objects.filter(user=request.user).first().board
	if not board:
		api_message = APIMessage(
			code=400,
			message="Bad request",
			details="User is not a member of any board"
		)
		return Response(data=api_message.to_dict(), status=status.HTTP_400_BAD_REQUEST)
	mutable_data = request.data.copy()  # Make a mutable copy
	mutable_data['board'] = board.id  # Modify the data
	serializer = self.get_serializer(data=mutable_data)
	serializer.is_valid(raise_exception=True)
	serializer.save()
	return Response(serializer.data, status=status.HTTP_201_CREATED)
	
	
