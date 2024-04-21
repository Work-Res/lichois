
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

from app_attachments.models import ApplicationAttachment
from app_attachments.api.serializers import ApplicationAttachmentSerializer
from app_attachments.classes import CreateNewApplicationAttachment


class ApplicationDocumentListView(viewsets.ModelViewSet):
    queryset = ApplicationAttachment.objects.all()
    serializer_class = ApplicationAttachmentSerializer
    lookup_field = 'document_number'

    def post(self, request, document_number, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            contact_creater = CreateNewApplicationAttachment(data=serializer.data)
            contact_creater.document_number = document_number
            contact_creater.create()
            if contact_creater.response.status:
                return Response(contact_creater.response.result(), status=status.HTTP_201_CREATED)
            else:
                return Response(contact_creater.response.result(), status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, document_number, *args, **kwargs):
        contacts = ApplicationAttachment.objects.filter(document_number=document_number)
        serializer = ApplicationAttachmentSerializer(contacts, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = ApplicationAttachment.objects.all()
        document_number = self.request.query_params.get('application_number')

        # Filter the queryset based on parameters
        if document_number:
            queryset = ApplicationAttachment.objects.filter(
                application_version__application__application_document__document_number=document_number)
        return queryset
