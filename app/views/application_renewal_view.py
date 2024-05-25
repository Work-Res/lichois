import logging

import json

from django.http import JsonResponse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.api import RenewalApplicationDTO
from app.classes import RenewalApplicationService
from app.api.serializers import ApplicationRenewalDTOSerializer

from ..exceptions import  ApplicationRenewalException

logger = logging.getLogger(__name__)


class ApplicationRenewalView(APIView):

    def post(self, request, format=None):
        try:
            serializer = ApplicationRenewalDTOSerializer(data=request.data)
            if serializer.is_valid():
                renewal_application_dto = RenewalApplicationDTO(**serializer.data)
                service = RenewalApplicationService(renewal_application=renewal_application_dto)
                service.process_renewal()
                return JsonResponse(service.response.result())
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except json.JSONDecodeError:
            logger.error("Invalid JSON in request body")
            return JsonResponse({'error': 'Invalid JSON in request body'}, status=status.HTTP_400_BAD_REQUEST)
        except ApplicationRenewalException as e:
            logger.error(f"ApplicationRenewalException: {str(e)}")
            return JsonResponse({'detail': f'Something went wrong. Got {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            return JsonResponse({'detail': f'Something went wrong. Got {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
