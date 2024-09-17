from rest_framework import viewsets
from ..models import LiftingAppliance
from ..api.serializers import LiftingApplianceSerializer


class LiftingApplianceViewSet(viewsets.ModelViewSet):
    queryset = LiftingAppliance.objects.all()
    serializer_class = LiftingApplianceSerializer
    