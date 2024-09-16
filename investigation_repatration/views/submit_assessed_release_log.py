import json
import logging

from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from ..classes import PrisonerReleaseLogBatchService

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class SubmitAssessedPrisonerReleaseLogView(APIView):

    def post(self, request):
        try:
            service = PrisonerReleaseLogBatchService()
            id = request.data.get("id")
            editable = request.data.get("editable")
            service.update_batch_editable(id, editable)
            return JsonResponse(service.response.result())
        except json.JSONDecodeError:
            logger.error("Invalid JSON in request body")
            return JsonResponse(
                {"error": "Invalid JSON in request body"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            return JsonResponse(
                {"detail": f"Something went wrong. Got {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
