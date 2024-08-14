from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response

from ..models import ApplicationAttachmentVerification
from ..api.serializers import ApplicationAttachmentVerificationSerializer


class ApplicationAttachmentVerificationView(viewsets.ModelViewSet):
    queryset = ApplicationAttachmentVerification.objects.all()
    serializer_class = ApplicationAttachmentVerificationSerializer
    lookup_field = "attachment"

    def get_queryset(self):
        attachment_id = self.kwargs.get("attachment")
        if attachment_id:
            return self.queryset.filter(attachment__id=attachment_id)
        return self.queryset

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        attachment = get_object_or_404(queryset, **kwargs)
        serializer = ApplicationAttachmentVerificationSerializer(attachment)
        return Response(serializer.data)
