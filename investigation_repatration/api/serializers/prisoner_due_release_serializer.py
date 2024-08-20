from rest_framework import serializers
from ...models import PrisonerDueRelease

class PrisonerDueReleaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrisonerDueRelease
        fields = '__all__'