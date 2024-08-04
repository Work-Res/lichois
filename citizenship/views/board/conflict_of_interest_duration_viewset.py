from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from citizenship.api.serializers.board import ConflictOfInterestDurationSerializer
from citizenship.models.board.conflict_of_interest_duration import ConflictOfInterestDuration


class ConflictOfInterestDurationViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing ConflictOfInterestDuration instances.
    """
    serializer_class = ConflictOfInterestDurationSerializer
    queryset = ConflictOfInterestDuration.objects.all()

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=['get'])
    def is_within_duration(self, request, pk=None):
        conflict_duration = self.get_object()
        within_duration = conflict_duration.is_within_duration()
        return Response({'is_within_duration': within_duration})
