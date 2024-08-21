from rest_framework import viewsets
from ..models import ExemptionUpliftmentStatus
from api.serializers import ExemptionUpliftmentStatusSerializer


class ExemptionUpliftmentStatusViewSet(viewsets.ModelViewSet):
    queryset = ExemptionUpliftmentStatus.objects.all()
    serializer_class = ExemptionUpliftmentStatusSerializer
