from rest_framework import viewsets

from ..api.serializers import ApplicationDecisionTypeSerializer
from ..models import ApplicationDecisionType


class ApplicationDecisionTypeViewSet(viewsets.ModelViewSet):
    queryset = ApplicationDecisionType.objects.all()
    serializer_class = ApplicationDecisionTypeSerializer
