from rest_framework import viewsets
from ..models import BoardMeeting
from ..serializers import BoardMeetingSerializer


class BoardMeetingViewSet(viewsets.ModelViewSet):
	queryset = BoardMeeting.objects.all()
	serializer_class = BoardMeetingSerializer
