import logging
import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.http import JsonResponse

from workresidentpermit.api.serializers import RequestDeferredApplicationDTOSerializer
from ..api.dto import RequestDeferredApplicationDTO

from ..classes.service import DeferredApplicationService

logger = logging.getLogger(__name__)


class DeferredApplicationView(APIView):

    def post(self, request, document_number):
        try:
            serializer = RequestDeferredApplicationDTOSerializer(data=request.data)
            if serializer.is_valid():
                request_deferred_application_dto = RequestDeferredApplicationDTO(**serializer.data)

                service = DeferredApplicationService(
                    request_deferred_application_dto=request_deferred_application_dto)
                if service.validate():
                    service.create()
                else:
                    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except json.JSONDecodeError:
            logger.error("Invalid JSON in request body")
            return JsonResponse({'error': 'Invalid JSON in request body'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            return JsonResponse({'detail': f'Something went wrong. Got {str(e)}'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CompleteDeferredApplicationView(APIView):
    """

    """
    def post(self, request, document_number):
        try:
            serializer = RequestDeferredApplicationDTOSerializer(data=request.data)
            if serializer.is_valid():
                request_deferred_application_dto = RequestDeferredApplicationDTO(**serializer.data)

                service = DeferredApplicationService(
                    request_deferred_application_dto=request_deferred_application_dto)
                if not service.validate():
                    service.complete_deferred_application()
                else:
                    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except json.JSONDecodeError:
            logger.error("Invalid JSON in request body")
            return JsonResponse({'error': 'Invalid JSON in request body'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            return JsonResponse({'detail': f'Something went wrong. Got {str(e)}'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
