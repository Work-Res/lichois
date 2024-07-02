from rest_framework import viewsets
from ..models import PermitCancellationReason
from ..api.serializers import PermitCancellationReasonSerializer


class PermitCancellationReasonViewSet(viewsets.ModelViewSet):
    queryset = PermitCancellationReason.objects.all()
    serializer_class = PermitCancellationReasonSerializer
