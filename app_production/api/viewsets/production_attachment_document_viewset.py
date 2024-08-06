from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import FileResponse

from app_production.api.serializers.production_attachment_document_serializer import \
    ProductionAttachmentDocumentSerializer
from app_production.models import ProductionAttachmentDocument


class ProductionAttachmentDocumentViewSet(viewsets.ModelViewSet):
    queryset = ProductionAttachmentDocument.objects.all()
    serializer_class = ProductionAttachmentDocumentSerializer

    @action(detail=False, methods=['get'], url_path='download/(?P<document_number>[^/.]+)')
    def download_by_number(self, request, document_number=None):
        try:
            document = ProductionAttachmentDocument.objects.get(document_number=document_number)
            response = FileResponse(
                document.pdf_document.open(), as_attachment=True, filename=document.pdf_document.name)
            return response
        except ProductionAttachmentDocument.DoesNotExist:
            return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)
