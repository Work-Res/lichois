from rest_framework import serializers

from app_address.api.serializers import ApplicationAddressSerializer
from ..models import ApplicantRelative


class ApplicantRelativeSerializer(serializers.ModelSerializer):
	# address = ApplicationAddressSerializer()
	
	class Meta:
		model = ApplicantRelative
		fields = '__all__'
