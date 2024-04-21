from rest_framework import viewsets
from lichois.visa.models import BlueCardApplication
from ..serializers import BlueCardApplicationSerializer


class BlueCardViewSet(viewsets.ModelViewSet):
    queryset = BlueCardApplication.objects.all()
    serializer_class = BlueCardApplicationSerializer
