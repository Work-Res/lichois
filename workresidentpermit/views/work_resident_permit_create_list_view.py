from rest_framework import viewsets

from ..models import WorkResidencePermit

from ..api.serializers import WorkResidencePermitSerializer


class WorkResidencePermitCreateListView(viewsets.ModelViewSet):
    queryset = WorkResidencePermit.objects.all()
    serializer_class = WorkResidencePermitSerializer
