from rest_framework import viewsets
from ..models import Boiler
from ..api.serializers import BoilerSerializer


class BoilerViewSet(viewsets.ModelViewSet):
    queryset = Boiler.objects.all()
    serializer_class = BoilerSerializer
    