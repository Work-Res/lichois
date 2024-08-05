from rest_framework import serializers
from ...models import AssessmentEmergency


class AssessmentEmergencySerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentEmergency
        fields = "__all__"
