from rest_framework import viewsets
from ..models import PrisonerDueRelease
from api.serializers import PrisonerDueReleaseSerializer

class PrisonerDueReleaseViewSet(viewsets.ModelViewSet):
    queryset = PrisonerDueRelease.objects.all()
    serializer_class = PrisonerDueReleaseSerializer