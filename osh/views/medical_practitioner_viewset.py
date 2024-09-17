from rest_framework import viewsets
from ..models import MedicalPractitioner
from ..api.serializers import MedicalPractitionerSerializer


class MedicalPractitionerViewSet(viewsets.ModelViewSet):
    queryset = MedicalPractitioner.objects.all()
    serializer_class = MedicalPractitionerSerializer
    