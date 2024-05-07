from rest_framework import viewsets
from ..models import CitizenshipBySettlement
from ..serializers import CitizenshipBySettlementSerializer


class CitizenshipBySettlementViewSet(viewsets.ModelViewSet):
    queryset = CitizenshipBySettlement.objects.all()
    serializer_class = CitizenshipBySettlementSerializer
