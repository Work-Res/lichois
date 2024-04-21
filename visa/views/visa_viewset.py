from rest_framework import viewsets
from ..models import Visa
from ..serializers import VisaSerializer


class VisaViewSet(viewsets.ModelViewSet):
    queryset = Visa.objects.all()
    serializer_class = VisaSerializer
