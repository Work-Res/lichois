from rest_framework import viewsets
from ..models import ApplicationContact
from ..api.serializers import ApplicationContactSerializer


class ApplicationContactViewSet(viewsets.ModelViewSet):
    queryset = ApplicationContact.objects.all()
    serializer_class = ApplicationContactSerializer
