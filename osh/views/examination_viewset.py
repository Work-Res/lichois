from rest_framework import viewsets
from ..models import Examination
from ..api.serializers import ExaminationSerializer


class ExaminationViewSet(viewsets.ModelViewSet):
    queryset = Examination.objects.all()
    serializer_class = ExaminationSerializer
    