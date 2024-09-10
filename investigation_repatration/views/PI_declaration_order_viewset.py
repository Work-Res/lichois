from rest_framework import viewsets

from ..api.serializers import (
    PIDeclarationOrderSerializer,
    PIDeclarationOrderAcknoledgementSerializer,
)
from ..models import PIDeclarationOrder, PIDeclarationOrderAcknowledgement


class PIDeclarationOrderViewSet(viewsets.ModelViewSet):
    queryset = PIDeclarationOrder.objects.all()
    serializer_class = PIDeclarationOrderSerializer


class PIDeclarationOrderAcknowledgementViewSet(viewsets.ModelViewSet):
    queryset = PIDeclarationOrderAcknowledgement.objects.all()
    serializer_class = PIDeclarationOrderAcknoledgementSerializer
