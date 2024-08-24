from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from app.api.common.pagination import StandardResultsSetPagination
from gazette.models import BatchApplication
from gazette.api.serializers import BatchApplicationGazetteSerializer
from gazette.views.filter import BatchApplicationFilter


class BatchApplicationViewSet(viewsets.ModelViewSet):
    queryset = BatchApplication.objects.all()
    serializer_class = BatchApplicationGazetteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BatchApplicationFilter
    pagination_class = StandardResultsSetPagination
