from rest_framework import viewsets
from ..models import TravelCertificate
from ..serializers import TravelCertificateSerializer


class TravelCertificateViewSet(viewsets.ModelViewSet):
	queryset = TravelCertificate.objects.all()
	serializer_class = TravelCertificateSerializer
