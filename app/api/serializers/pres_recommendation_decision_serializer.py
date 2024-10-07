from rest_framework import serializers

from app.models import PresRecommendationDecision


class PresRecommendationDecisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PresRecommendationDecision
        fields = [
            'document_number',
            'date_requested',
            'date_approved',
            'status',
            'approved_by',
            'role',
        ]
