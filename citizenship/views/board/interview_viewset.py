from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from django.core.exceptions import ValidationError

from app.api.common.pagination import StandardResultsSetPagination
from citizenship.api.serializers.board import InterviewSerializer
from citizenship.models import Interview
from citizenship.service.board.interview_service import InterviewService
from citizenship.views.board.filter import InterviewFilter


class InterviewViewSet(viewsets.ModelViewSet):
    queryset = Interview.objects.all()
    serializer_class = InterviewSerializer
    filterset_class = InterviewFilter
    pagination_class = StandardResultsSetPagination

    @action(detail=False, methods=['post'], url_path='update-by-application')
    def update_by_application(self, request):
        application_id = request.data.get('application_id')
        conducted = request.data.get('conducted')
        status_value = request.data.get('status')

        if not application_id:
            return Response({"error": "Application ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        if conducted is None or status_value is None:
            return Response({"error": "Both conducted and status fields are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            service = InterviewService()
            interview = service.update_interview_by_application_id(application_id, conducted, status_value)
            serializer = self.get_serializer(interview)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "Unexpected error occurred: " + str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
