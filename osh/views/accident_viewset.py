from rest_framework import viewsets
from ..models import Accident
from ..api.serializers import AccidentSerializer


class AccidentViewSet(viewsets.ModelViewSet):
    queryset = Accident.objects.all()
    serializer_class = AccidentSerializer
    