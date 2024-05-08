from rest_framework import viewsets
from ..models import LateCitizenshipRenunciation
from ..serializers import LateCitizenshipRenunciationSerializer


class LateCitizenshipRenunciationViewSet(viewsets.ModelViewSet):
    queryset = LateCitizenshipRenunciation.objects.all()
    serializer_class = LateCitizenshipRenunciationSerializer
