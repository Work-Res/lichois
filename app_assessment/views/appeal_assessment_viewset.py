from rest_framework import viewsets

from app_assessment.api.serializers import AppealAssessmentSerializer
from app_assessment.models import AppealAssessment


class AppealAssessmentViewSet(viewsets.ModelViewSet):
    queryset = AppealAssessment.objects.all()
    serializer_class = AppealAssessmentSerializer
