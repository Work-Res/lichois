from rest_framework import serializers
from ...models import PermitReplacement


class PermitReplacementSerializer(serializers.ModelSerializer):
	class Meta:
		model = PermitReplacement
		fields = '__all__'
