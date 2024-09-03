from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from app.api.common.pagination import StandardResultsSetPagination
from citizenship.api.serializers.board import ConflictOfInterestDurationSerializer
from citizenship.models.board.conflict_of_interest_duration import ConflictOfInterestDuration
from citizenship.views.board.filter import ConflictOfInterestDurationFilter


class ConflictOfInterestDurationViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing ConflictOfInterestDuration instances.
    """
    serializer_class = ConflictOfInterestDurationSerializer
    queryset = ConflictOfInterestDuration.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = ConflictOfInterestDurationFilter
    pagination_class = StandardResultsSetPagination


    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=['get'])
    def is_within_duration(self, request, pk=None):
        conflict_duration = self.get_object()
        within_duration = conflict_duration.is_within_duration()
        return Response({'is_within_duration': within_duration})
