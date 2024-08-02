from django.utils import timezone

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from app.api.common.web import APIMessage
from citizenship.api.serializers.board import MeetingSerializer, AttendeeSerializer

from citizenship.models import Meeting

from citizenship.service.board import MeetingService

from citizenship.utils.parse_datetime_with_timezone import parse_datetime_with_timezone


class MeetingViewSet(viewsets.ModelViewSet):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        data = serializer.data
        title = validated_data['title']
        board_id = validated_data['board'].id
        location = validated_data['location']
        agenda = validated_data['agenda']
        start_date = validated_data['start_date']
        end_date = validated_data['end_date']
        time = validated_data['time']

        try:
            meeting = MeetingService.create_meeting(
                title=title,
                board_id=board_id,
                location=location,
                agenda=agenda,
                start_date=start_date,
                end_date=end_date,
                time=time
            )
            api_message = APIMessage(
                code=201,
                message="Board Meeting is created",
                details=f"Board Meeting is created for {meeting.id}",
            )

            return Response(api_message.to_dict(), status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

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
