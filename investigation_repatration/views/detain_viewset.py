from rest_framework import viewsets
from ..models import Detain
from api.serializers import DetainSerializer


class DetainViewSet(viewsets.ModelViewSet):
    queryset = Detain.objects.all()
    serializer_class = DetainSerializer
