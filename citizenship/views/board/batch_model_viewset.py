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
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'])
    def remove_application(self, request, pk=None):
        batch = self.get_object()
        application_id = request.data.get('application_id')
        try:
            BatchService.remove_application_from_batch(batch_id=batch.id, application_id=application_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'])
    def declare_no_conflict_for_all(self, request, pk=None):
        attendee_id = request.user
        meeting_session_id = request.data.get('meeting_session_id')
        try:
            BatchService.declare_no_conflict_for_all(
                attendee_id=attendee_id, batch_id=pk, meeting_session=meeting_session_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'])
    def change_status(self, request, pk=None):
        batch = self.get_object()
        new_status = request.data.get('new_status')
        try:
            updated_batch = BatchService.change_batch_status(batch_id=batch.id, new_status=new_status)
            return Response(BatchSerializer(updated_batch).data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'])
    def declare_conflict_of_interest(self, request, pk=None):
        attendee_id = request.user
        document_number = request.data.get('document_number')
        has_conflict = request.data.get('has_conflict', False)
        meeting_session_id = request.data.get('meeting_session_id')
        client_relationship = request.data.get('client_relationship')
        interest_description = request.data.get('interest_description')

        try:
            BatchService.declare_conflict_of_interest(
                attendee_id=attendee_id,
                document_number=document_number,
                has_conflict=has_conflict,
                meeting_session=meeting_session_id,
                client_relationship=client_relationship,
                interest_description=interest_description
            )
            return Response({'detail': 'Conflict of interest declared successfully'}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
