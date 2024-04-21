from rest_framework import serializers
from ...models import Permit, Child, Spouse, WorkResidencePermit


class PermitSerializer(serializers.ModelSerializer):

    place_issue = serializers.CharField(min_length=3, allow_blank=False, trim_whitespace=True, required=True)
    permit_type = serializers.CharField(min_length=3, allow_blank=False, trim_whitespace=True, required=True)

    class Meta:
        model = Permit
        fields = (
            'permit_type',
            'permit_no',
            'date_issued',
            'date_expiry',
            'place_issue',
        )
        extra_kwargs = {
            'date_issued': {'format': 'iso-8601'},
            'date_expiry': {'format': 'iso-8601'}
        }
