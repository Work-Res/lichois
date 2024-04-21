from rest_framework import serializers
from ...models import ResidencePermitCancellation


class ResidencePermitCancellationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResidencePermitCancellation
        fields = '__all__'
        