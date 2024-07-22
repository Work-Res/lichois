from rest_framework import viewsets
from ..models import DependantAssessment
from ..api.serializers import DependantAssessmentSerializer


class DependantAssessmentViewSet(viewsets.ModelViewSet):
    queryset = DependantAssessment.objects.all()
    serializer_class = DependantAssessmentSerializer
