from rest_framework import serializers

from app_decision.api.serializers import ApplicationDecisionTypeSerializer
from ...models import CommissionerDecision


class CommissionerDecisionSerializer(serializers.ModelSerializer):
	status = ApplicationDecisionTypeSerializer()
	
	class Meta:
		model = CommissionerDecision
		fields = (
			'date_requested',
			'date_approved',
			'status',
			'summary'
		)
