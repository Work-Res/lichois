from rest_framework import viewsets
from ..models import ApplicantExperience
from ..api.serializers import ApplicantExperienceSerializer


class ApplicantExperienceViewSet(viewsets.ModelViewSet):
    queryset = ApplicantExperience.objects.all()
    serializer_class = ApplicantExperienceSerializer
    