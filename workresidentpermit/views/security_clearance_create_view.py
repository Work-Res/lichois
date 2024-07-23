import logging

import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.http import JsonResponse

from ..api.serializers import SecurityClearanceRequestDTOSerializer
from ..api.dto import SecurityClearanceRequestDTO

from ..validators import SecurityClearanceValidator
from ..classes import SecurityClearanceService

logger = logging.getLogger(__name__)


class SecurityClearanceCreateAPIView(APIView):
    """
    Responsible for creating an security clearance record
    POST
        {
            document_number = document_number
            status = pending # list of valid options ['pending', 'Rejected', 'Accepted'],
            summary="text"
        }
    """

    def post(self, request, document_number):
        try:
            serializer = SecurityClearanceRequestDTOSerializer(data=request.data)
            if serializer.is_valid():
                security_clearance_request = SecurityClearanceRequestDTO(
                    **serializer.data
                )
                validator = SecurityClearanceValidator(
                    document_number=document_number,
                    status=security_clearance_request.status,
                )
                if validator.is_valid():
                    service = SecurityClearanceService(
                        security_clearance_request=security_clearance_request
                    )
                    service.create_clearance()
                    return JsonResponse(service.response.result())
                else:
                    return JsonResponse(
                        validator.response.result(), status=status.HTTP_400_BAD_REQUEST
                    )
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
