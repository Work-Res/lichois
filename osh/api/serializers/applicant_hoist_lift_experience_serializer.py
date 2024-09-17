from rest_framework import serializers
from ...models import ApplicantHoistLiftExperience


class ApplicantHoistLiftExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicantHoistLiftExperience
        fields = "__all__"
