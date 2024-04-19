from rest_framework import viewsets

from ..models import Spouse
from ..api.serializers import SpouseSerializer


class SpouseCreateListView(viewsets.ModelViewSet):
    queryset = Spouse.objects.all()
    serializer_class = SpouseSerializer
