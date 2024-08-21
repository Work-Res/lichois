from rest_framework import serializers
from ...models import ExemptionUpliftmentStatus

class ExemptionUpliftmentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExemptionUpliftmentStatus
        fields = '__all__'

