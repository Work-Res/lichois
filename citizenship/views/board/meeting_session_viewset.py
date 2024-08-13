from rest_framework import viewsets

from app.api.common.pagination import StandardResultsSetPagination
from citizenship.api.serializers.board import MeetingSessionSerializer
from citizenship.models import MeetingSession
from citizenship.views.board.filter import MeetingSessionFilter


class MeetingSessionViewSet(viewsets.ModelViewSet):
    queryset = MeetingSession.objects.all()
    serializer_class = MeetingSessionSerializer
    filterset_class = MeetingSessionFilter
    pagination_class = StandardResultsSetPagination
