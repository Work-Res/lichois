from rest_framework import viewsets
from ..models import ApplicationStatus
from ..api.serializers import ApplicationStatusSerializer


class ApplicationStatusViewSet(viewsets.ModelViewSet):
    queryset = ApplicationStatus.objects.all()
    serializer_class = ApplicationStatusSerializer
