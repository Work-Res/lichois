from rest_framework import viewsets

from ..api.serializers import ProhibitedImmigrantSerializer
from ..models import ProhibitedImmigrant


class ProhibitedImmigrantViewSet(viewsets.ModelViewSet):
    queryset = ProhibitedImmigrant.objects.all()
    serializer_class = ProhibitedImmigrantSerializer
