from rest_framework import viewsets
from ..models import ApplicantConstructionExperience
from ..api.serializers import ApplicantConstructionExperienceSerializer


class ApplicantConstructionExperienceViewSet(viewsets.ModelViewSet):
    queryset = ApplicantConstructionExperience.objects.all()
    serializer_class = ApplicantConstructionExperienceSerializer
    