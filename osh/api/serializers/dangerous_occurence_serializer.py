from rest_framework import serializers
from ...models import DangerousOccurence


class DangerousOccurenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DangerousOccurence
        fields = "__all__"
