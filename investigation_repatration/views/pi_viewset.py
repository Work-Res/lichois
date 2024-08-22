from rest_framework import viewsets
from ..models import ProhibitedImmigrant
from api.serializers import ProhibitedImmigrantSerializer


class ProhibitedImmigrantViewSet(viewsets.ModelViewSet):
    queryset = ProhibitedImmigrant.objects.all()
    serializer_class = ProhibitedImmigrantSerializer
