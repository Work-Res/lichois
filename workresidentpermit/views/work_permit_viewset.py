from rest_framework import viewsets
from ..models import WorkPermit
from ..api.serializers import WorkPermitSerializer


class WorkPermitViewSet(viewsets.ModelViewSet):
    queryset = WorkPermit.objects.all()
    serializer_class = WorkPermitSerializer
    lookup_field = "document_number"
