from rest_framework import viewsets
from ..models import MeetingAttendee
from ..serializers import MeetingAttendeeSerializer


class MeetingAttendeeViewSet(viewsets.ModelViewSet):
	queryset = MeetingAttendee.objects.all()
	serializer_class = MeetingAttendeeSerializer
