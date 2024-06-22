from rest_framework import viewsets
from ..models import TravelCertificatePermit
from ..serializers import TravelCertificatePermitSerializer


class TravelCertificatePermitViewSet(viewsets.ModelViewSet):
    queryset = TravelCertificatePermit.objects.all()
    serializer_class = TravelCertificatePermitSerializer
