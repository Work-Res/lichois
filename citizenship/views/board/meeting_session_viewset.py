from rest_framework import viewsets

from app.api.common.pagination import StandardResultsSetPagination
from citizenship.api.serializers.board import MeetingSessionSerializer
from citizenship.models import MeetingSession


class MeetingSessionViewSet(viewsets.ModelViewSet):
    queryset = MeetingSession.objects.all()
    serializer_class = MeetingSessionSerializer
    pagination_class = StandardResultsSetPagination
