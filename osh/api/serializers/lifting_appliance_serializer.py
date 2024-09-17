from rest_framework import serializers
from ...models import LiftingAppliance


class LiftingApplianceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiftingAppliance
        fields = "__all__"
