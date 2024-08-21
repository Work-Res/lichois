from rest_framework import viewsets
from ..models import PIRecommendation
from api.serializers import PIRecommendationSerializer

class PIRecommendationViewSet(viewsets.ModelViewSet):
    queryset = PIRecommendation.objects.all()
    serializer_class = PIRecommendationSerializer
