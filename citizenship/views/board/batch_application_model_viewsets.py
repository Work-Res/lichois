from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from app.api.common.pagination import StandardResultsSetPagination
from citizenship.api.serializers.board import BatchApplicationCitizenshipSerializer
from citizenship.models import BatchApplication
from citizenship.views.board.filter import BatchApplicationFilter


class BatchApplicationViewSet(viewsets.ModelViewSet):
    queryset = BatchApplication.objects.all()
    serializer_class = BatchApplicationCitizenshipSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BatchApplicationFilter
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        # Custom validation can be handled here if needed before saving
        serializer.save()

    def perform_update(self, serializer):
        # Handle updates, with any custom logic you need
        serializer.save()
