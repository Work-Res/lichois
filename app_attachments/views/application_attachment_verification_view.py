from rest_framework import viewsets
from ..models import ApplicationAttachmentVerification
from ..api.serializers import ApplicationAttachmentVerificationSerializer


class ApplicationAttachmentVerificationView(viewsets.ModelViewSet):
    queryset = ApplicationAttachmentVerification.objects.all()
    serializer_class = ApplicationAttachmentVerificationSerializer
    lookup_field = 'attachment'
