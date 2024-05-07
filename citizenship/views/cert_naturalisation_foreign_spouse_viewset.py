from rest_framework import viewsets
from ..models import CertNaturalisationByForeignSpouse
from ..serializers import CertNaturalisationByForeignSpouseSerializer


class CertNaturalisationByForeignSpouseViewSet(viewsets.ModelViewSet):
    queryset = CertNaturalisationByForeignSpouse.objects.all()
    serializer_class = CertNaturalisationByForeignSpouseSerializer
