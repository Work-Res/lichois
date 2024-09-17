from rest_framework import serializers
from ...models import Appointee


class AppointeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointee
        fields = "__all__"
