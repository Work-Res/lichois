from rest_framework import serializers
from ...models import PIRecommendation


class PIRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PIRecommendation
        fields = '__all__'