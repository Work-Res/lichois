from rest_framework import viewsets
from ..models import Bearer
from ..api.serializers import BearerSerializer


class BearerViewSet(viewsets.ModelViewSet):
    queryset = Bearer.objects.all()
    serializer_class = BearerSerializer
    