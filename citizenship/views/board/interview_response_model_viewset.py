import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
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

    def get_queryset(self):
        """
        Override the default get_queryset to apply filtering based on the request.
        """
        queryset = super().get_queryset()

        # Initialize filterset with the request data and current queryset
        filterset = self.filterset_class(self.request.GET, queryset=queryset, request=self.request)

        # If the filterset is valid, return the filtered queryset
        if filterset.is_valid():
            return filterset.qs

        # Fallback to returning the full queryset if no filtering is applied
        return queryset

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

    @action(detail=False, methods=['get'], url_path='by-interview')
    def get_responses_by_interview(self, request, *args, **kwargs):
        """
        Custom action to retrieve InterviewResponse objects filtered by the interview ID.
        The interview ID should be passed as a query parameter.
        Example: /interviewresponses/by-interview/?interview=<interview_id>
        """
        interview_id = request.query_params.get('interview')
        if not interview_id:
            return Response({'detail': 'Interview ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Filter InterviewResponse by the interview ID
            responses = InterviewResponse.objects.filter(interview__id=interview_id, member__user=request.user)

            if not responses.exists():
                return Response({'detail': 'No responses found for the provided interview ID.'},
                                status=status.HTTP_404_NOT_FOUND)

            # Paginate and serialize the filtered responses
            page = self.paginate_queryset(responses)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(responses, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ValidationError as e:
            logger.warning(f"Validation error when fetching responses for interview ID {interview_id} - {str(e)}")
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(f"An error occurred while fetching responses for interview ID {interview_id} - {str(e)}")
            return Response({'detail': 'An unexpected error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['put'], url_path='bulk-update')
    def bulk_update(self, request, *args, **kwargs):
        data = request.data

        logger.info("Received request for bulk update of InterviewResponses")

        try:
            updated_responses, is_valid = InterviewResponseService.bulk_update_interview_responses(data)
            if is_valid:
                logger.info("Successfully performed bulk update of InterviewResponses")
                return Response(updated_responses, status=status.HTTP_200_OK)
            else:
                return Response(updated_responses, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            logger.warning(f"Validation error during bulk update of InterviewResponses - {str(e)}")
            return Response({'detail': f"{str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(f"An unexpected error occurred during bulk update of InterviewResponses. Got, {str(e)}")
            return Response({'detail': 'An unexpected error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)