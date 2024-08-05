from rest_framework import serializers
from ...models import DependantAssessment


class DependantAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DependantAssessment
        fields = "__all__"
