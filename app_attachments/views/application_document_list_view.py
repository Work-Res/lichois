from rest_framework import generics

from app_attachments.models import ApplicationAttachment
from app_attachments.api.serializers import ApplicationAttachmentSerializer


class ApplicationDocumentListView(generics.ListAPIView):

    serializer_class = ApplicationAttachmentSerializer

    def get_queryset(self):
        queryset = ApplicationAttachment.objects.all()
        document_number = self.request.query_params.get('application_number')

        # Filter the queryset based on parameters
        if document_number:
            queryset = ApplicationAttachment.objects.filter(
                application_version__application__application_document__document_number=document_number)
        return queryset
