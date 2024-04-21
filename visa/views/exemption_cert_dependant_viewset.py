from rest_framework import viewsets
from lichois.visa.models import ExemptionCertificateDependant
from ..serializers import ExemptionCertificateDependantSerializer


class ExemptionCertificateDependantViewSet(viewsets.ModelViewSet):
    queryset = ExemptionCertificateDependant.objects.all()
    serializer_class = ExemptionCertificateDependantSerializer
