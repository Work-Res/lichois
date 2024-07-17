from rest_framework import viewsets

from citizenship.api.serializers.certificate_of_origin_serializer import CertificateOfOriginSerializer
from citizenship.models.renunciation import CertificateOfOrigin


class CertificateOfOriginViewSet(viewsets.ModelViewSet):
    queryset = CertificateOfOrigin.objects.all()
    serializer_class = CertificateOfOriginSerializer
    lookup_field = 'document_number'

