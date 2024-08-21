from rest_framework import serializers
from ...models import PIUpliftmentRecommendation

class PIUpliftmentRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PIUpliftmentRecommendation
        fields = '__all__'
