from rest_framework import viewsets

from . import ApplicationRenewalHistoryFilter
from ..models import ApplicationRenewalHistory
from ..api.serializers import ApplicationRenewalHistorySerializer


class ApplicationRenewalHistoryView(viewsets.ModelViewSet):

    queryset = ApplicationRenewalHistory.objects.all()
    serializer_class = ApplicationRenewalHistorySerializer
    filterset_class = ApplicationRenewalHistoryFilter
