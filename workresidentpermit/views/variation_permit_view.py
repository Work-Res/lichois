from rest_framework import viewsets

from ..models import VariationPermit
from ..api.serializers import VariationPermitSerializer


class VariationPermitViewSet(viewsets.ModelViewSet):
    queryset = VariationPermit.objects.all()
    serializer_class = VariationPermitSerializer
