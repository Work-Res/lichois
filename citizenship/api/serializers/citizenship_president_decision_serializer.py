from rest_framework import serializers

from citizenship.models import CitizenshipPresidentDecision


class CitizenshipPresidentDecisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CitizenshipPresidentDecision
        fields = [
            'document_number',
            'date_requested',
            'date_approved',
            'status',
            'approved_by'
        ]
