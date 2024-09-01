from rest_framework import serializers
from app_assessment.models import ReviewCaseDecision


class ReviewCaseDecisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewCaseDecision
        fields = '__all__'
