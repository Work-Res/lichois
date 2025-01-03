from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.http import FileResponse
import os

from gazette.models import BatchApplication
from gazette.service import GenerateGazettePDFService, PrepareGazetteForDownload


class DownloadGazettePDFAPIView(APIView):

    def get(self, request, batch_id):
        now = datetime.now()
        formatted_date = now.strftime("%Y-%m-%d")

        word_file_name = f"gazette-{formatted_date}.docx"
        pdf_file_name = "gazette.pdf"
        word_file_path = os.path.join(settings.MEDIA_ROOT, word_file_name)
        pdf_file_path = os.path.join(settings.MEDIA_ROOT, pdf_file_name)

        # Retrieve all batch applications related to the given batch_id
        batch_applications = BatchApplication.objects.filter(batch__id=batch_id)

        if not batch_applications.exists():
            return Response({"detail": "No batch applications found."}, status=status.HTTP_404_NOT_FOUND)

        # Prepare the data
        prepare_download_data = PrepareGazetteForDownload(batch_applications=batch_applications)
        data = prepare_download_data.prepared_data()

        # Initialize the PDF generation service with the prepared data
        service = GenerateGazettePDFService(data, word_file_path, pdf_file_path)

        # Generate the PDF document
        service.create_word_document()

        # Check if the file was created successfully
        if os.path.exists(pdf_file_path):
            # Serve the PDF file for download
            response = FileResponse(open(pdf_file_path, 'rb'), as_attachment=True, filename="gazette.docx")
            response['Content-Disposition'] = f'attachment; filename="gazette_{batch_id}.docx"'
            return response
        else:
            return Response({"detail": "File not found."}, status=status.HTTP_404_NOT_FOUND)
