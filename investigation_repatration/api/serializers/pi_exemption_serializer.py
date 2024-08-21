from rest_framework import serializers
from ...models import PIExemption

class PIExemptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PIExemption
        fields = '__all__'
