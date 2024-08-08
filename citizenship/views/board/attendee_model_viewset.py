from rest_framework import viewsets

from citizenship.api.serializers.board import AttendeeSerializer
from citizenship.models import Attendee
from citizenship.views.board.filter import AttendeeFilter


class AttendeeViewSet(viewsets.ModelViewSet):
    queryset = Attendee.objects.all()
    serializer_class = AttendeeSerializer
    filterset_class = AttendeeFilter
