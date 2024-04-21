from rest_framework import viewsets
from lichois.visa.models import ExemptionCertificate
from ..serializers import ExemptionCertificateSerializer


class ExemptionCertificateViewSet(viewsets.ModelViewSet):
    queryset = ExemptionCertificate.objects.all()
    serializer_class = ExemptionCertificateSerializer
