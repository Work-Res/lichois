from rest_framework import serializers
from ...models import InjuredPerson


class InjuredPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = InjuredPerson
        fields = "__all__"
