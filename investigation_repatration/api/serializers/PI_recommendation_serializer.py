from rest_framework import serializers
from ...models import AssessmentRecommendation


class AssessmentRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentRecommendation
        fields = '__all__'