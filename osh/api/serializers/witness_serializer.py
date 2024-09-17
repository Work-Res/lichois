from rest_framework import serializers
from ...models import Witness


class WitnessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Witness
        fields = "__all__"
