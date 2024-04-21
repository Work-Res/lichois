from rest_framework import viewsets
from ..models import ExemptionCertificate
from ..api.serializers import ExemptionCertificateSerializer


class ExemptionCertificateViewSet(viewsets.ModelViewSet):
	queryset = ExemptionCertificate.objects.all()
	serializer_class = ExemptionCertificateSerializer
