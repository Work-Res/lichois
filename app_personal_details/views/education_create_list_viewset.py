from rest_framework import viewsets
from ..models import Education
from ..api.serializers import EducationSerializer


class EducationViewSet(viewsets.ModelViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
