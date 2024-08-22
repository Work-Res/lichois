from rest_framework import viewsets
from ..models import DetentionWarrant
from api.serializers import DetentionWarrantSerializer


class DetentionWarrantViewSet(viewsets.ModelViewSet):
    queryset = DetentionWarrant.objects.all()
    serializer_class = DetentionWarrantSerializer
