from rest_framework import viewsets
from ..models import PrisonerDueForRelease
from api.serializers import PrisonerDetailsSerializer

class PrisonerDetailsViewSet(viewsets.ModelViewSet):
    queryset = PrisonerDueForRelease.objects.all()
    serializer_class = PrisonerDetailsSerializer