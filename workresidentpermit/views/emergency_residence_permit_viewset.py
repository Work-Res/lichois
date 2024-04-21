from rest_framework import viewsets
from ..models import EmergencyResidencePermit
from ..api.serializers import EmergencyResidencePermitSerializer


class EmergencyResidencePermitViewSet(viewsets.ModelViewSet):
	queryset = EmergencyResidencePermit.objects.all()
	serializer_class = EmergencyResidencePermitSerializer
