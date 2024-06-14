from rest_framework import viewsets

from workresidentpermit.api.serializers import CommissionerDecisionSerializer
from workresidentpermit.models import CommissionerDecision


class CommissionerDecisionViewSet(viewsets.ModelViewSet):
	queryset = CommissionerDecision.objects.all()
	serializer_class = CommissionerDecisionSerializer
