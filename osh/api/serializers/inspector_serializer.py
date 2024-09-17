from rest_framework import serializers
from ...models import Inspector


class InspectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inspector
        fields = "__all__"
