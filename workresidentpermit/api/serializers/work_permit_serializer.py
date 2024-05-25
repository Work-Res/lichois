from rest_framework import serializers

from app.api.serializers import ApplicationVersionSerializer
from workresidentpermit.models import WorkPermit


class WorkPermitSerializer(serializers.ModelSerializer):

	class Meta:
		model = WorkPermit
		fields = '__all__'
