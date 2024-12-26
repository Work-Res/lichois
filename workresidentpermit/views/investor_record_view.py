from rest_framework import viewsets

from ..models import InvestorRecord
from ..api.serializers import InvestorRecordSerializer


class InvestorRecordViewSet(viewsets.ModelViewSet):
    queryset = InvestorRecord.objects.all()
    serializer_class = InvestorRecordSerializer
