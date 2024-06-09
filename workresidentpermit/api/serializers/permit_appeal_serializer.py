from rest_framework import serializers
from ...models import PermitAppeal


class PermitAppealSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermitAppeal
        fields = '__all__'
        