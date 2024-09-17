from rest_framework import viewsets
from ..models import Inspector
from ..api.serializers import InspectorSerializer


class InspectorViewSet(viewsets.ModelViewSet):
    queryset = Inspector.objects.all()
    serializer_class = InspectorSerializer
    