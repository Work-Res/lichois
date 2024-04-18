from rest_framework import generics
from app_attachments.models import ApplicationAttachment

from app_attachments.api.serializers import ApplicationAttachmentSerializer


class ApplicationAttachmentDeleteView(generics.DestroyAPIView):
    queryset = ApplicationAttachment.objects.all()
    serializer_class = ApplicationAttachmentSerializer
