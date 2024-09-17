from rest_framework import viewsets
from ..models import Premise
from ..api.serializers import PremiseSerializer


class PremiseViewSet(viewsets.ModelViewSet):
    queryset = Premise.objects.all()
    serializer_class = PremiseSerializer
    