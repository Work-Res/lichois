from rest_framework import serializers
from ...models import PrisonerReleaseLog


class PrisonerReleaseLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrisonerReleaseLog
        fields = "__all__"
