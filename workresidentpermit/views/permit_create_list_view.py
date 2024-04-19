from rest_framework import viewsets

from ..models import Permit
from ..api.serializers import PermitSerializer


class PermitCreateListView(viewsets.ModelViewSet):
    queryset = Permit.objects.all()
    serializer_class = PermitSerializer
