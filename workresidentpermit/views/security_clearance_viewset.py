from rest_framework import viewsets
from workresidentpermit.models import SecurityClearance
from workresidentpermit.api.serializers import SecurityClearanceSerializer


class SecurityClearanceViewSet(viewsets.ModelViewSet):
    queryset = SecurityClearance.objects.all()
    serializer_class = SecurityClearanceSerializer
