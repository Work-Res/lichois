from rest_framework import viewsets
from ..models import ExemptionCertificate
from ..serializers import VisaExemptionCertSerializer


class ExemptionCertificateViewSet(viewsets.ModelViewSet):
    queryset = ExemptionCertificate.objects.all()
    serializer_class = VisaExemptionCertSerializer
