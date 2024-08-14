import logging

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from app.api.common.pagination import StandardResultsSetPagination
from citizenship.api.serializers.board import ConflictOfInterestSerializer
from citizenship.models import ConflictOfInterest
from citizenship.views.board.filter import ConflictOfInterestFilter
from citizenship.service.board import ConflictOfInterestService

logger = logging.getLogger(__name__)


class ConflictOfInterestViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing ConflictOfInterest instances.
    """
    serializer_class = ConflictOfInterestSerializer
    queryset = ConflictOfInterest.objects.all()
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = ConflictOfInterestFilter

    @action(detail=True, methods=['post'])
    def declare_conflict(self, request, pk=None):
        conflict = self.get_object()
        conflict.has_conflict = True
        conflict.save()
        return Response({'status': 'conflict declared'})

    @action(detail=True, methods=['post'])
    def resolve_conflict(self, request, pk=None):
        conflict = self.get_object()
        conflict.has_conflict = False
        conflict.save()
        return Response({'status': 'conflict resolved'})

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
