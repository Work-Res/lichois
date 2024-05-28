import logging

import json

from drf_yasg.utils import swagger_auto_schema

from django.http import JsonResponse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..classes.dto import ApplicationBatchRequestDTO
from ..classes import ApplicationBatchService
from ..serializers import ApplicationBatchRequestDTOSerializer

from ..validators import ApplicationBatchValidator


logger = logging.getLogger(__name__)


class ApplicationBatchCreateView(APIView):
    
    """
    Responsible for creating an application batch.
    POST
        {
            "batch_type": "work_resident_permit",
            "applications": [
                "83cfbe58-2a53-4f35-a28a-c53081980588"
            ],
            "batch_duration": ""
        }
    """

    @swagger_auto_schema(methods=['post'], request_body=ApplicationBatchRequestDTOSerializer)
    def post(self, request, format=None):
        try:
            serializer = ApplicationBatchRequestDTOSerializer(data=request.data)
            if serializer.is_valid():
                application_batch_dto = ApplicationBatchRequestDTO(**serializer.data)
                validator = ApplicationBatchValidator(application_batch_request=application_batch_dto)
                if validator.is_valid():
                    service = ApplicationBatchService(application_batch_request=application_batch_dto)
                    service.create_batch()
                    return JsonResponse(service.response.result())
                else:
                    return JsonResponse(validator.response.result(), status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except json.JSONDecodeError:
            logger.error("Invalid JSON in request body")
            return JsonResponse({'error': 'Invalid JSON in request body'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            return JsonResponse({'detail': f'Something went wrong. Got {str(e)}'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
