from rest_framework import serializers
from ...models import PermitCancellationReason


class PermitCancellationReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermitCancellationReason
        fields = '__all__'
