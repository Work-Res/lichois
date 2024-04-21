from rest_framework import serializers
from ...models import EmergencyResidencePermit


class EmergencyResidencePermitSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyResidencePermit
        fields = '__all__'
        