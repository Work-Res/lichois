from rest_framework import serializers
from ...models import PenaltyDecision

class PenaltyDecisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PenaltyDecision
        fields = '__all__'

