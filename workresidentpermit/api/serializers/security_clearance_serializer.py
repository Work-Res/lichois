from rest_framework import serializers
from workresidentpermit.models import SecurityClearance

from .work_residence_permit_serializer import WorkResidencePermitSerializer


class SecurityClearanceSerializer(serializers.ModelSerializer):

    work_resident_permit = WorkResidencePermitSerializer()

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
