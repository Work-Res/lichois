from rest_framework import viewsets
from ..models import Appointee
from ..api.serializers import AppointeeSerializer


class AppointeeViewSet(viewsets.ModelViewSet):
    queryset = Appointee.objects.all()
    serializer_class = AppointeeSerializer
    