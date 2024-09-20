from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import FileResponse
from rest_framework import status
from django.shortcuts import get_object_or_404

from app_production.models import ProductionAttachmentDocument


class ProductionAttachmentDocumentDownloadView(APIView):

    def get(self, request, document_number):
        # Check if document_number is provided and is not None or empty
        if not document_number:
            return Response({'error': 'Document number is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Get the document based on document_number
            document = get_object_or_404(ProductionAttachmentDocument, document_number=document_number)

            # Return the PDF document as a downloadable file
            response = FileResponse(
                document.pdf_document.open(), as_attachment=True, filename=document.pdf_document.name)
            return response
        except ProductionAttachmentDocument.DoesNotExist:
            # Return a 404 response if the document is not found
            return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Catch any other errors
            return Response({'error': f'Unexpected error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
