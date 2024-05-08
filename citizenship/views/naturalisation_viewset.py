from rest_framework import viewsets
from ..models import Naturalisation
from ..serializers import NaturalisationSerializer


class NaturalisationViewSet(viewsets.ModelViewSet):
    queryset = Naturalisation.objects.all()
    serializer_class = NaturalisationSerializer
