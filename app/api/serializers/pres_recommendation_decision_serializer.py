from rest_framework import serializers

from app.models import PresRecommendationDecision


class PresRecommendationDecisionSerializer(serializers.ModelSerializer):

    document_number = serializers.CharField(max_length=200, required=True)
    status = serializers.CharField(max_length=200, required=True)
    summary = serializers.CharField(max_length=500, required=False, allow_blank=True)

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
