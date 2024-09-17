from rest_framework import viewsets
from ..models import Witness
from ..api.serializers import WitnessSerializer


class WitnessViewSet(viewsets.ModelViewSet):
    queryset = Witness.objects.all()
    serializer_class = WitnessSerializer
    