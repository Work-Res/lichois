from rest_framework import serializers
from ...models import AppealAssessment


class AppealAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppealAssessment
        fields = "__all__"
