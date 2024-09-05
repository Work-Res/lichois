from rest_framework import serializers

from app_decision.models import ApplicationDecisionType
from citizenship.models import RecommendationDecision


class RecommendationDecisionSerializer(serializers.ModelSerializer):
    status = serializers.SlugRelatedField(
        slug_field='name',  # Assuming the ApplicationDecisionType model has a 'name' field
        queryset=ApplicationDecisionType.objects.all()
    )

    class Meta:
        model = RecommendationDecision
        fields = [
            'id',  # Assuming BaseUuidModel includes an 'id' field
            'document_number',
            'date_requested',
            'date_approved',
            'status',
            'approved_by'
        ]
