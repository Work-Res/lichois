from rest_framework import viewsets
from ..models import OathOfAllegiance
from ..serializers import OathOfAllegianceSerializer


class OathOfAllegianceViewSet(viewsets.ModelViewSet):
    queryset = OathOfAllegiance.objects.all()
    serializer_class = OathOfAllegianceSerializer
