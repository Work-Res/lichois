from rest_framework import viewsets

from django_filters.rest_framework import DjangoFilterBackend
from app.api.common.pagination import StandardResultsSetPagination
from .filters import OathOfAllegianceFilter

from ..models import OathOfAllegiance
from citizenship.api.serializers import OathOfAllegianceSerializer


class OathOfAllegianceViewSet(viewsets.ModelViewSet):
    queryset = OathOfAllegiance.objects.all()
    serializer_class = OathOfAllegianceSerializer
    pagination_class = StandardResultsSetPagination
    filterset_class = OathOfAllegianceFilter
    filter_backends = [DjangoFilterBackend]
