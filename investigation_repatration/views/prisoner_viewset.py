from rest_framework import viewsets
from ..models import Prisoner
from api.serializers import PrisonerSerializer


class PrisonerViewSet(viewsets.ModelViewSet):
    queryset = Prisoner.objects.all()
    serializer_class = PrisonerSerializer
