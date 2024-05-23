from rest_framework import viewsets
from ..models import OathOfAllegiance
from lichois.citizenship.api.serializers import OathOfAllegianceSerializer


class OathOfAllegianceViewSet(viewsets.ModelViewSet):
    queryset = OathOfAllegiance.objects.all()
    serializer_class = OathOfAllegianceSerializer
