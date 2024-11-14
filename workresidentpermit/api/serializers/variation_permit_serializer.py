from rest_framework import serializers

from workresidentpermit.models import VariationPermit


class VariationPermitSerializer(serializers.ModelSerializer):

    class Meta:
        model = VariationPermit
        fields = "__all__"
