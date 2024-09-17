from rest_framework import viewsets
from ..models import Defect
from ..api.serializers import DefectSerializer


class DefectViewSet(viewsets.ModelViewSet):
    queryset = Defect.objects.all()
    serializer_class = DefectSerializer
    