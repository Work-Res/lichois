from rest_framework import viewsets
from ..models import InjuredPerson
from ..api.serializers import InjuredPersonSerializer


class InjuredPersonViewSet(viewsets.ModelViewSet):
    queryset = InjuredPerson.objects.all()
    serializer_class = InjuredPersonSerializer
    