import logging
from rest_framework import viewsets, status
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend
from django.core.exceptions import ValidationError
from app.api.common.pagination import StandardResultsSetPagination
from citizenship.api.serializers.board import InterviewResponseSerializer
from citizenship.models import InterviewResponse
from citizenship.service.board import InterviewResponseService
from citizenship.views.board.filter import InterviewResponseFilter

logger = logging.getLogger(__name__)


class InterviewResponseViewSet(viewsets.ModelViewSet):
    queryset = InterviewResponse.objects.all()
    serializer_class = InterviewResponseSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = InterviewResponseFilter

    def update(self, request, *args, **kwargs):
        response_id = kwargs.get('pk')
        data = request.data

        logger.info(f"Received request to update InterviewResponse with id: {response_id}")

        try:
            updated_response = InterviewResponseService.update_interview_response(response_id, data)
            logger.info(f"Successfully updated InterviewResponse with id: {response_id}")
            return Response(updated_response, status=status.HTTP_200_OK)
        except ValidationError as e:
            logger.warning(f"Validation error while updating InterviewResponse with id: {response_id} - {str(e)}")
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(
                f"An unexpected error occurred while updating InterviewResponse with id: {response_id} - {str(e)}")
            return Response({'detail': 'An unexpected error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
