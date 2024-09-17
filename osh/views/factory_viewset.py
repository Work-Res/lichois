from rest_framework import viewsets
from ..models import Factory
from ..api.serializers import FactorySerializer


class FactoryViewSet(viewsets.ModelViewSet):
    queryset = Factory.objects.all()
    serializer_class = FactorySerializer
    