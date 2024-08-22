from rest_framework import viewsets
from ..models import DetentionDetails
from api.serializers import DetentionDetailsSerializer


class DetentionDetailsViewSet(viewsets.ModelViewSet):
    queryset = DetentionDetails.objects.all()
    serializer_class = DetentionDetailsSerializer
