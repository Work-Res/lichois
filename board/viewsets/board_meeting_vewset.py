from rest_framework import status, viewsets
from rest_framework.response import Response

from app.api.common.web import APIMessage
from ..models import BoardMeeting, BoardMember
from ..serializers import BoardMeetingSerializer


class BoardMeetingViewSet(viewsets.ModelViewSet):
	queryset = BoardMeeting.objects.all()
	serializer_class = BoardMeetingSerializer
	
	
