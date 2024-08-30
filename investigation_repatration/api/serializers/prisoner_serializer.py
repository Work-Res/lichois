from rest_framework import serializers
from ...models import Prisoner

class PrisonerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prisoner
        fields = '__all__'
