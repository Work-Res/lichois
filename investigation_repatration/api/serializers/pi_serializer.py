from rest_framework import serializers
from ...models import ProhibitedImmigrant


class ProhibitedImmigrantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProhibitedImmigrant
        fields = "__all__"
