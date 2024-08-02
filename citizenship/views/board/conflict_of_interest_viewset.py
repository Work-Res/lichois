from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from citizenship.api.serializers.board import ConflictOfInterestSerializer
from citizenship.models import ConflictOfInterest


class ConflictOfInterestViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing ConflictOfInterest instances.
    """
    serializer_class = ConflictOfInterestSerializer
    queryset = ConflictOfInterest.objects.all()

    @action(detail=True, methods=['post'])
    def declare_conflict(self, request, pk=None):
        conflict = self.get_object()
        conflict.has_conflict = True
        conflict.save()
        return Response({'status': 'conflict declared'})

    @action(detail=True, methods=['post'])
    def resolve_conflict(self, request, pk=None):
        conflict = self.get_object()
        conflict.has_conflict = False
        conflict.save()
        return Response({'status': 'conflict resolved'})
