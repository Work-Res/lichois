from rest_framework import viewsets
from ..models import VisaReference
from ..serializers import VisaReferenceSerializer


class VisaReferenceViewSet(viewsets.ModelViewSet):
    queryset = VisaReference.objects.all()
    serializer_class = VisaReferenceSerializer
