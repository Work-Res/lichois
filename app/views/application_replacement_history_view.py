from rest_framework import viewsets

from . import ApplicationRenewalHistoryFilter
from .filters.application_replacement_history_filter import ApplicationReplacementHistoryFilter
from ..api.common.pagination import StandardResultsSetPagination

from ..api.serializers.application_replacement_serializer import ApplicationReplacementHistorySerializer
from ..models import ApplicationReplacementHistory


class ApplicationReplacementHistoryView(viewsets.ModelViewSet):

    queryset = ApplicationReplacementHistory.objects.all()
    serializer_class = ApplicationReplacementHistorySerializer
    filterset_class = ApplicationReplacementHistoryFilter
    pagination_class = StandardResultsSetPagination
