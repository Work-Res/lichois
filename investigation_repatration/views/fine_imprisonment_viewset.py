from rest_framework import viewsets
from ..models import PenaltyDecision
from api.serializers import PenaltyDecisionSerializer


class PenaltyDecisionViewSet(viewsets.ModelViewSet):
    queryset = PenaltyDecision.objects.all()
    serializer_class = PenaltyDecisionSerializer
