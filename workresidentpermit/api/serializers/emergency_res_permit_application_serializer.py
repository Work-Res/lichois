from rest_framework import serializers
from ...models import EmergencyResPermitApplication


class EmergencyResPermitApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyResPermitApplication
        fields = '__all__'
        