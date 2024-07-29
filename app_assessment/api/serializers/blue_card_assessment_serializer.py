from rest_framework import serializers

from ...models import BlueCardAssessment


class BlueCardAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlueCardAssessment
        fields = "__all__"
