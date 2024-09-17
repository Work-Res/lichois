from rest_framework import serializers
from ...models import HeatTreatment

class ApplicantConstructionExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeatTreatment        
        fields = "__all__"
