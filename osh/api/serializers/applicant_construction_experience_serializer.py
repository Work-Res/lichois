from rest_framework import serializers
from ...models import ApplicantConstructionExperience


class ApplicantConstructionExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicantConstructionExperience
        fields = "__all__"
