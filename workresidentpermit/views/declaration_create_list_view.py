from rest_framework import viewsets
from workresidentpermit.models import Declaration

from ..api.serializers import DeclarationSerializer


class DeclarationViewSet(viewsets.ModelViewSet):
    queryset = Declaration.objects.all()
    serializer_class = DeclarationSerializer
