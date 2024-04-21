from rest_framework import viewsets
from ..models import EmergencyResPermitApplication
from ..api.serializers import EmergencyResPermitApplicationSerializer


class EmergencyResPermitApplicationViewSet(viewsets.ModelViewSet):
	queryset = EmergencyResPermitApplication.objects.all()
	serializer_class = EmergencyResPermitApplicationSerializer
