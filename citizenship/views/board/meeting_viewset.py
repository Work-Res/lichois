import logging

from django.utils import timezone
from django.db import transaction

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from app.api.common.pagination import StandardResultsSetPagination
from app.api.common.web import APIMessage
from citizenship.api.serializers.board import MeetingSerializer, AttendeeSerializer, MeetingSessionSerializer

from citizenship.models import Meeting

from citizenship.service.board import MeetingService

from citizenship.utils.parse_datetime_with_timezone import parse_datetime_with_timezone
from citizenship.views.board.filter import MeetingFilter

logger = logging.getLogger(__name__)


class MeetingViewSet(viewsets.ModelViewSet):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
    filterset_class = MeetingFilter
    pagination_class = StandardResultsSetPagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        print("testing testing..", validated_data)
        try:
            with transaction.atomic():
                meeting = MeetingService.create_meeting(**validated_data)
            api_message = APIMessage(
                code=201,
                message="Board Meeting is created",
                details=f"Board Meeting is created for {meeting.id}",
            )
            return Response(api_message.to_dict(), status=status.HTTP_201_CREATED)

        except ValidationError as e:
            logger.warning(f"Validation error during meeting creation: {str(e)}")
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error during meeting creation: {str(e)}", exc_info=True)
            return Response(
                {'detail': 'An unexpected error occurred while creating the meeting.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def list(self, request, *args, **kwargs):
        meetings = self.get_queryset()
        serialized_meetings = MeetingSerializer(meetings, many=True).data

        for meeting in serialized_meetings:
            start_date = parse_datetime_with_timezone(meeting['start_date'])
            end_date = parse_datetime_with_timezone(meeting['end_date'])

            # Ensure start_date and end_date are timezone-aware
            if start_date.tzinfo is None or start_date.tzinfo.utcoffset(start_date) is None:
                start_date = timezone.make_aware(start_date)
            if end_date.tzinfo is None or end_date.tzinfo.utcoffset(end_date) is None:
                end_date = timezone.make_aware(end_date)

            # Convert to UTC
            meeting['start_date'] = start_date.astimezone(timezone.utc).isoformat()
            meeting['end_date'] = end_date.astimezone(timezone.utc).isoformat()

        return Response(serialized_meetings, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def add_attendee(self, request, pk=None):
        meeting = self.get_object()
        member_id = request.data.get('member_id')
        confirmed = request.data.get('confirmed', False)
        attendee = MeetingService.add_attendee(meeting.id, member_id, confirmed)
        return Response(AttendeeSerializer(attendee).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def remove_attendee(self, request, pk=None):
        meeting = self.get_object()
        member_id = request.data.get('member_id')
        MeetingService.remove_attendee(meeting.id, member_id)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def change_status(self, request, pk=None):
        meeting = self.get_object()
        new_status = request.data.get('status')
        meeting = MeetingService.change_meeting_status(meeting.id, new_status)
        return Response(MeetingSerializer(meeting).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def confirm_attendance(self, request, pk=None):
        meeting = self.get_object()
        member_id = request.data.get('member_id')
        confirmed = request.data.get('confirmed', False)
        proposed_date = request.data.get('proposed_date')
        attendee = MeetingService.confirm_attendance(meeting.id, member_id, confirmed, proposed_date)
        return Response(MeetingSerializer(attendee).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def create_session(self, request, pk=None):
        meeting = self.get_object()
        serializer = MeetingSessionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        title = serializer.validated_data['title']
        date = serializer.validated_data['date']
        start_time = serializer.validated_data['start_time']
        end_time = serializer.validated_data['end_time']

        try:
            session = MeetingService.create_session(meeting.id, title, date, start_time, end_time)
            return Response(MeetingSessionSerializer(session).data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
