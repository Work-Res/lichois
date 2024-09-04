from rest_framework import serializers
from ...models import PrisonerReleaseLog


class PrisonerReleaseLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrisonerReleaseLog
        fields = "__all__"


class PrisonerBatchRequestDTOSerializer(serializers.Serializer):

    prisoners = serializers.ListField(
        child=serializers.CharField(max_length=200),
        required=True,
    )
