from rest_framework import viewsets

from app_assessment.api.serializers import AssessmentEmergencySerializer
from app_assessment.models import AssessmentEmergency


class AssessmentEmergencyViewSet(viewsets.ModelViewSet):
    queryset = AssessmentEmergency.objects.all()
    serializer_class = AssessmentEmergencySerializer
