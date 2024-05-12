from rest_framework import viewsets
from ..models import BlueCardApplication
from ..serializers import BlueCardApplicationSerializer


class BlueCardApplicationViewSet(viewsets.ModelViewSet):
    queryset = BlueCardApplication.objects.all()
    serializer_class = BlueCardApplicationSerializer