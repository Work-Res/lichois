from rest_framework import viewsets
from ..models import BoilerFitting
from ..api.serializers import BoilerFittingSerializer


class BoilerFittingViewSet(viewsets.ModelViewSet):
    queryset = BoilerFitting.objects.all()
    serializer_class = BoilerFittingSerializer
    