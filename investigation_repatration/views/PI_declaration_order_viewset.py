from rest_framework import viewsets

from ..api.serializers import PIDeclarationOrderSerializer
from ..models import PIDeclarationOrder


class PIDeclarationOrderViewSet(viewsets.ModelViewSet):
    queryset = PIDeclarationOrder.objects.all()
    serializer_class = PIDeclarationOrderSerializer
