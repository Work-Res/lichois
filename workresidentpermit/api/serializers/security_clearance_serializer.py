from rest_framework import serializers
from ...models import SecurityClearance

from .residence_permit_serializer import ResidencePermitSerializer


class SecurityClearanceSerializer(serializers.ModelSerializer):

    # work_resident_permit = WorkResidencePermitSerializer()

    class Meta:
        model = SecurityClearance
        fields = (
            'id',
            'work_resident_permit',
            'date_requested',
            'date_approved',
            'status',
            'summary'
        )
