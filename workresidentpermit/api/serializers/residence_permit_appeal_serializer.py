from rest_framework import serializers
from ...models import ResidencePermitAppeal


class ResidencePermitAppealSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResidencePermitAppeal
        fields = '__all__'
        