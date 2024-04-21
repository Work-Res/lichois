from rest_framework import viewsets
from lichois.visa.models import ExemptionCertificateApplication
from ..serializers import ExemptionCertificateApplicationSerializer


class ExemptionCertificateApplicationViewSet(viewsets.ModelViewSet):
    queryset = ExemptionCertificateApplication.objects.all()
    serializer_class = ExemptionCertificateApplicationSerializer
