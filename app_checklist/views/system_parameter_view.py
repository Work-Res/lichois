from rest_framework import viewsets

from ..api.serializers import SystemParameterSerializer
from ..models import SystemParameter
from django_filters import rest_framework as filters
from ..filters import SystemParameterFilter

class SystemParameterViewSet(viewsets.ModelViewSet):
    queryset = SystemParameter.objects.all()
    serializer_class = SystemParameterSerializer
    filter_backends = (filters.DjangoFilterBackend,)  
    filterset_class = SystemParameterFilter 
