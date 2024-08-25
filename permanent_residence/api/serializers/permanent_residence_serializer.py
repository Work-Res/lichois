from rest_framework import serializers
from ...models import PermanentResidence


class PermanentResidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermanentResidence
        fields = "__all__"
