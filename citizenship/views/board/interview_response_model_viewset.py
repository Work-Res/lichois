import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.core.exceptions import ValidationError
from app.api.common.pagination import StandardResultsSetPagination
from citizenship.api.serializers.board import InterviewResponseSerializer
from citizenship.models import InterviewResponse
from citizenship.service.board import InterviewResponseService, ConflictOfInterestService
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

    @action(detail=True, methods=['post'], url_path='authorize-member')
    def authorize_member_for_interview(self, request, pk=None):
        """
        Authorizes a board member with a declared conflict of interest to participate in the interview.
        """
        attendee_id = request.data.get('attendee_id')
        application_id = request.data.get('application_id')

        logger.info(f"Received request to authorize member for interview with attendee ID: "
                    f"{attendee_id} and application ID: {application_id}")

        try:
            conflict_of_interest = ConflictOfInterestService.authorize_member_for_interview(attendee_id, application_id)
            logger.info(
                f"Member {conflict_of_interest.attendee.member.user.username} authorized to participate in the interview "
                f"for application {conflict_of_interest.application}."
            )
            return Response({
                'message': 'Member authorized successfully.',
                'conflict_of_interest': {
                    'id': conflict_of_interest.id,
                    'member': conflict_of_interest.attendee.member.user.username,
                    'application': conflict_of_interest.application.application_document.document_number,
                    'is_authorized': conflict_of_interest.is_authorized
                }
            }, status=status.HTTP_200_OK)
        except ValidationError as e:
            logger.warning(f"Validation error while authorizing member: {str(e)}")
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(f"An unexpected error occurred during member authorization: {str(e)}")
            return Response({'detail': 'An unexpected error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
