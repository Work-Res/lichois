from rest_framework import viewsets
from ..models import BoardDecision
from ..serializers import BoardDecisionSerializer


class BoardDecisionViewSet(viewsets.ModelViewSet):
	queryset = BoardDecision.objects.all()
	serializer_class = BoardDecisionSerializer
