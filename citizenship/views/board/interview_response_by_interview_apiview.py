import logging

from rest_framework import generics, status
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from citizenship.api.serializers.board import InterviewResponseSerializer
from citizenship.models import InterviewResponse

logger = logging.getLogger(__name__)


class InterviewResponseByInterviewAPIView(generics.ListAPIView):
    """
    API to retrieve InterviewResponse objects filtered by interview ID.
    """
    serializer_class = InterviewResponseSerializer

    def get_queryset(self):
        interview_id = self.request.query_params.get('interview')

        if not interview_id:
            return InterviewResponse.objects.none()

        try:
            # Filter by interview ID and the request user
            return InterviewResponse.objects.filter(interview__id=interview_id, member__user=self.request.user)
        except ValidationError as e:
            logger.warning(f"Validation error while fetching responses for interview ID {interview_id}: {str(e)}")
            return InterviewResponse.objects.none()

    def list(self, request, *args, **kwargs):
        """
        Override the list method to add custom validation and response handling.
        """
        interview_id = request.query_params.get('interview')

        if not interview_id:
            return Response({'detail': 'Interview ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        queryset = self.get_queryset()

        if not queryset.exists():
            return Response({'detail': 'No responses found for the provided interview ID.'},
                            status=status.HTTP_404_NOT_FOUND)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)