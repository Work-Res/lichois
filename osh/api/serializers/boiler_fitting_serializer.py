from rest_framework import serializers
from ...models import BoilerFitting


class BoilerFittingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoilerFitting
        fields = "__all__"
