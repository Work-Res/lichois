from rest_framework import viewsets
from ..models import AssessmentRecommendation
from api.serializers import AssessmentRecommendationSerializer

class AssessmentRecommendationViewSet(viewsets.ModelViewSet):
    queryset = AssessmentRecommendation.objects.all()
    serializer_class = AssessmentRecommendationSerializer
