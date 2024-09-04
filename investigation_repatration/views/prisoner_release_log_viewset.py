from rest_framework import viewsets
from ..models import PrisonerReleaseLog
from ..api.serializers import PrisonerReleaseLogSerializer


class PrisonerReleaseLogViewSet(viewsets.ModelViewSet):
    queryset = PrisonerReleaseLog.objects.all()
    serializer_class = PrisonerReleaseLogSerializer
