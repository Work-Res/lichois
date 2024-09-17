from rest_framework import serializers
from ...models import Appointer


class AppointerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointer
        fields = "__all__"
