from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.exceptions import ValidationError

from app.api.common.pagination import StandardResultsSetPagination
from citizenship.api.serializers.board import BatchSerializer

from citizenship.models import Batch
from citizenship.service.board import BatchService


class BatchModelViewSet(viewsets.ModelViewSet):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer
    pagination_class = StandardResultsSetPagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        batch = BatchService.create_batch(
            meeting_id=serializer.validated_data['meeting'].id,
            name=serializer.validated_data['name']
        )
        return Response(BatchSerializer(batch).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def add_application(self, request, pk=None):
        batch = self.get_object()
        document_number = request.data.get('document_number')
        session_id = request.data.get('session_id')
        try:
            BatchService.add_application_to_batch(
                batch_id=batch.id, document_number=document_number, session_id=session_id)
            return Response(status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def add_applications(self, request, pk=None):
        batch = self.get_object()
        document_numbers = request.data.get('document_numbers', [])
        session_id = request.data.get('session_id')
        try:
            BatchService.add_applications_to_batch(
                batch_id=batch.id, document_numbers=document_numbers,
                session_id=session_id)
            return Response(status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def remove_application(self, request, pk=None):
        batch = self.get_object()
        application_id = request.data.get('application_id')
        try:
            BatchService.remove_application_from_batch(batch_id=batch.id, application_id=application_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def declare_no_conflict_for_all(self, request, pk=None):
        attendee_id = request.data.get('attendee_id')
        meeting_session_id = request.data.get('meeting_session_id')
        try:
            BatchService.declare_no_conflict_for_all(
                attendee_id=attendee_id, batch_id=pk, meeting_session=meeting_session_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
