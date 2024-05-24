from rest_framework import viewsets

from ..models import ApplicationVerification
from ..api.serializers import ApplicationVerificationSerializer


class ApplicationVerificationCreateListView(viewsets.ModelViewSet):
    queryset = ApplicationVerification.objects.all()
    serializer_class = ApplicationVerificationSerializer
    lookup_field = 'document_number'
