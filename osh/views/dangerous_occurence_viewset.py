from rest_framework import viewsets
from ..models import DangerousOccurence
from ..api.serializers import DangerousOccurenceSerializer


class DangerousOccurenceViewSet(viewsets.ModelViewSet):
    queryset = DangerousOccurence.objects.all()
    serializer_class = DangerousOccurenceSerializer
    