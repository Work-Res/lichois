from rest_framework import viewsets
from ..models import  PIDeclarationOrder
from api.serializers import PIDeclarationOrderSerializer

class PIDeclarationOrderViewSet(viewsets.ModelViewSet):
    queryset = PIDeclarationOrder.objects.all()
    serializer_class = PIDeclarationOrderSerializer
