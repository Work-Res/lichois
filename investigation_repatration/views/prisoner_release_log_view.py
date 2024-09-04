from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..api.serializers import (
    PrisonerBatchRequestDTOSerializer,
    PrisonerReleaseLogSerializer,
)
from ..classes.prisoner_batch_service import PrisonerReleaseLogBatchService
from ..models import PrisonerReleaseLog

import json

import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class PrisonerReleaseLogView(APIView):

    def get(self, request, *args, **kwargs):
        queryset = PrisonerReleaseLog.objects.all()
        serializer = PrisonerReleaseLogSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):

        try:
            serializer = PrisonerBatchRequestDTOSerializer(data=request.data)
            if serializer.is_valid():
                service = PrisonerReleaseLogBatchService(prisoner_batch=serializer.data)
                service.create_batch()
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
