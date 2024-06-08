from rest_framework import serializers
from ...models import PermitCancellation


class PermitCancellationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermitCancellation
        fields = '__all__'
        