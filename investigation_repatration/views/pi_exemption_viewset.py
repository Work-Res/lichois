from rest_framework import viewsets
from ..models import PIExemption
from api.serializers import PIExemptionSerializer


class PIExemptionViewSet(viewsets.ModelViewSet):
    queryset = PIExemption.objects.all()
    serializer_class = PIExemptionSerializer
