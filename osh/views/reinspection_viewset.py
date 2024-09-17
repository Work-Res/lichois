from rest_framework import viewsets
from ..models import Reinspection
from ..api.serializers import ReinspectionSerializer


class ReinspectionViewSet(viewsets.ModelViewSet):
    queryset = Reinspection.objects.all()
    serializer_class = ReinspectionSerializer
    