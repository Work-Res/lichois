from rest_framework import viewsets
from ..models import ExemptionCertificateApplication
from ..serializers import VisaExemptionCertificateAppSerializer


class ExemptionCertificateApplicationViewSet(viewsets.ModelViewSet):
    queryset = ExemptionCertificateApplication.objects.all()
    serializer_class = VisaExemptionCertificateAppSerializer
