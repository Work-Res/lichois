from rest_framework import serializers
from ...models import MedicalPractitioner


class MedicalPractitionerSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalPractitioner
        fields = "__all__"
