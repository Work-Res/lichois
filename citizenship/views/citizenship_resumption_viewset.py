from rest_framework import viewsets
from ..models import CitizenshipResumption
from ..serializers import CitizenshipResumptionSerializer


class CitizenshipResumptionViewSet(viewsets.ModelViewSet):
    queryset = CitizenshipResumption.objects.all()
    serializer_class = CitizenshipResumptionSerializer
