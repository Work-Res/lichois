from rest_framework import serializers
from ...models import Bearer


class BearerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bearer
        fields = "__all__"
