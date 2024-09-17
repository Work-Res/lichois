from rest_framework import viewsets
from ..models import Qualification
from ..api.serializers import QualificationSerializer


class QualificationViewSet(viewsets.ModelViewSet):
    queryset = Qualification.objects.all()
    serializer_class = QualificationSerializer
    