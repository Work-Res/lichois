from rest_framework import serializers
from ...models import ApplicantExperience


class ApplicantExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicantExperience
        fields = "__all__"
