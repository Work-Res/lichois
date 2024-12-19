from rest_framework import viewsets

from ..models import SeasonalFarmWorker
from ..api.serializers import SeasonalFarmWorkerSerializer


class SeasonalFarmWorkerViewSet(viewsets.ModelViewSet):
    queryset = SeasonalFarmWorker.objects.all()
    serializer_class = SeasonalFarmWorkerSerializer
