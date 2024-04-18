from rest_framework import viewsets

from ..api.serializers import ApplicationDecisionSerializer
from ..models import ApplicationDecision


class ApplicationDecisionViewSet(viewsets.ModelViewSet):
    queryset = ApplicationDecision.objects.all()
    serializer_class = ApplicationDecisionSerializer
