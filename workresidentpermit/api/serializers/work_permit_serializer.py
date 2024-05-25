from rest_framework import serializers

from workresidentpermit.models import WorkPermit


class WorkPermitSerializer(serializers.ModelSerializer):

	class Meta:
		model = WorkPermit
		fields = '__all__'
