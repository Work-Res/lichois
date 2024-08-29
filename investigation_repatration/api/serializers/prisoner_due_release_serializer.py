from rest_framework import serializers
from ...models import PrisonerDueForRelease

class PrisonerDueReleaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrisonerDueForRelease
        fields = '__all__'