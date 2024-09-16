from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import FileResponse, Http404

from citizenship.models.renunciation import RenunciationAttachment


class DownloadRenunciationAttachmentView(APIView):

    def get(self, request, document_number):
        try:
            # Fetch the attachment by ID
            attachment = RenunciationAttachment.objects.get(document_number=document_number)

            # Open the file for reading
            file_handle = attachment.document.open()

            # Create a FileResponse for downloading the file
            response = FileResponse(file_handle, as_attachment=True, filename=attachment.document.name)
            return response
        except RenunciationAttachment.DoesNotExist:
            raise Http404("Renunciation attachment not found.")
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
