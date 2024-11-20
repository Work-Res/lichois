from rest_framework import viewsets

from .application_appeal_history_filter import ApplicationAppealHistoryFilter
from ..api.common.pagination import StandardResultsSetPagination
from ..api.serializers.renewal_application_serializer import ApplicationAppealHistorySerializer
from ..models.application_appeal_history import ApplicationAppealHistory


class ApplicationAppealHistoryView(viewsets.ModelViewSet):

    queryset = ApplicationAppealHistory.objects.all()
    serializer_class = ApplicationAppealHistorySerializer
    filterset_class = ApplicationAppealHistoryFilter
    pagination_class = StandardResultsSetPagination
