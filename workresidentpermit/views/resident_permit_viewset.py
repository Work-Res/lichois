from rest_framework import viewsets

from ..models import ResidencePermit
from ..api.serializers import ResidencePermitSerializer


class ResidencePermitViewSet(viewsets.ModelViewSet):
    queryset = ResidencePermit.objects.all()
    serializer_class = ResidencePermitSerializer
    lookup_field = "document_number"
