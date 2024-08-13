from rest_framework import serializers
from ...models import SummaryAssessment


class SummaryAssessmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = SummaryAssessment
        fields = "__all__"
