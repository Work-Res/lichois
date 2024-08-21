from rest_framework import viewsets
from ..models import UpliftmentDecision
from api.serializers import UpliftmentDecisionSerializer


class UpliftmentDecisionViewSet(viewsets.ModelViewSet):
    queryset = UpliftmentDecision.objects.all()
    serializer_class = UpliftmentDecisionSerializer
