from rest_framework import viewsets
from ..models import PIUpliftmentRecommendation
from api.serializers import PIUpliftmentRecommendationSerializer


class PIUpliftmentRecommendationViewSet(viewsets.ModelViewSet):
    queryset = PIUpliftmentRecommendation.objects.all()
    serializer_class = PIUpliftmentRecommendationSerializer
