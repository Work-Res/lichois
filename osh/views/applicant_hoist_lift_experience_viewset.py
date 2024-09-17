from rest_framework import viewsets
from ..models import ApplicantHoistLiftExperience
from ..api.serializers import ApplicantHoistLiftExperienceSerializer


class ApplicantHoistLiftExperienceViewSet(viewsets.ModelViewSet):
    queryset = ApplicantHoistLiftExperience.objects.all()
    serializer_class = ApplicantHoistLiftExperienceSerializer
    