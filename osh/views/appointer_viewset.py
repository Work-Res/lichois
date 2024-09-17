from rest_framework import viewsets
from ..models import Appointer
from ..api.serializers import AppointerSerializer


class AppointerViewSet(viewsets.ModelViewSet):
    queryset = Appointer.objects.all()
    serializer_class = AppointerSerializer
    