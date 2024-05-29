from rest_framework import serializers
from ...models import SecurityClearance


class SecurityClearanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = SecurityClearance
        fields = (
            'date_requested',
            'date_approved',
            'status',
            'summary'
        )
