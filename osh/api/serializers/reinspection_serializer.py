from rest_framework import serializers
from ...models import Reinspection


class ReinspectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reinspection
        fields = "__all__"
