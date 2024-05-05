from rest_framework import viewsets
from ..models import AssessmentResult
from ..api.serializers import AssessmentResultSerializer


class AssessmentResultViewSet(viewsets.ModelViewSet):
    queryset = AssessmentResult.objects.all()
    serializer_class = AssessmentResultSerializer
