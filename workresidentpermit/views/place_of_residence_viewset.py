from rest_framework import viewsets
from ..models import PlaceOfResidence, SpousePlaceOfResidence
from ..api.serializers import PlaceOfResidenceSerializer


class PlaceOfResidenceViewSet(viewsets.ModelViewSet):
    queryset = PlaceOfResidence.objects.all()
    serializer_class = PlaceOfResidenceSerializer


class SpousePlaceOfResidenceViewSet(viewsets.ModelViewSet):
    queryset = SpousePlaceOfResidence.objects.all()
    serializer_class = PlaceOfResidenceSerializer
