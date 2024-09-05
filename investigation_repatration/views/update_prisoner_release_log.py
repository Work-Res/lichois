import json
import logging

from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..api.serializers import PrisonerReleaseLogSerializer
from ..classes import PrisonerReleaseLogBatchService

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class UpdatePrisonerReleaseLogView(APIView):

    def put(self, request, id, *args, **kwargs):
        try:
            serializer = PrisonerReleaseLogSerializer(data=request.data)
            if serializer.is_valid():
                service = PrisonerReleaseLogBatchService(prisoner_batch=serializer.data)
                service.update_batch(id)
                return JsonResponse(service.response.result())
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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
