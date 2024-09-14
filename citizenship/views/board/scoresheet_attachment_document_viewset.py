from rest_framework.views import APIView

from citizenship.models import ScoreSheet

from rest_framework.response import Response
from rest_framework import status
from django.http import FileResponse


class ScoresheetAttachmentDocumentView(APIView):

    def get(self, request, document_number=None):
        if not document_number:
            return Response({'error': 'Document number is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            document = ScoreSheet.objects.get(document_number=document_number)
            response = FileResponse(
                document.document.open(), as_attachment=True, filename=document.pdf_document.name
            )
            return response
        except ScoreSheet.DoesNotExist:
            return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)
