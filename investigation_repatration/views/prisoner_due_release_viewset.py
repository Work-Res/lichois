from rest_framework import viewsets
from ..models import PrisonerDueForRelease
from ..api.serializers import PrisonerDueReleaseSerializer


class PrisonerDueReleaseViewSet(viewsets.ModelViewSet):
    queryset = PrisonerDueForRelease.objects.all()
    serializer_class = PrisonerDueReleaseSerializer
