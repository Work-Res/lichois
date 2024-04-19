from rest_framework import viewsets

from ..models import Child
from ..api.serializers import ChildSerializer


class ChildCreateListView(viewsets.ModelViewSet):
    queryset = Child.objects.all()
    serializer_class = ChildSerializer
