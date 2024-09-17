from rest_framework import serializers
from ...models import Boiler


class BoilerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boiler
        fields = "__all__"
