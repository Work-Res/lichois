from rest_framework import viewsets
from lichois.visa.models import VisaApplication
from ..serializers import VisaApplicationSerializer


class VisaApplicationViewSet(viewsets.ModelViewSet):
    queryset = VisaApplication.objects.all()
    serializer_class = VisaApplicationSerializer
