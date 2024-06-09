from rest_framework import serializers
from ...models import EmergencyPermit


class EmergencyPermitSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyPermit
        fields = '__all__'
        