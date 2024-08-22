from rest_framework import viewsets
from ..models import Statement
from api.serializers import StatementSerializer


class StatementViewSet(viewsets.ModelViewSet):
    queryset = Statement.objects.all()
    serializer_class = StatementSerializer
