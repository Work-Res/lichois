from rest_framework import serializers
from ...models import UpliftmentDecision

class UpliftmentDecisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UpliftmentDecision
        fields = '__all__'

