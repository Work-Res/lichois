from rest_framework import viewsets
from ..models import HeatTreatment
from ..api.serializers import HeatTreatmentSerializer


class HeatTreatmentViewSet(viewsets.ModelViewSet):
    queryset = HeatTreatment.objects.all()
    serializer_class = HeatTreatmentSerializer
    