from rest_framework import viewsets

from ..api.serializers import SystemParameterSerializer
from ..models import SystemParameter


class SystemParameterViewSet(viewsets.ModelViewSet):
    queryset = SystemParameter.objects.all()
    serializer_class = SystemParameterSerializer
