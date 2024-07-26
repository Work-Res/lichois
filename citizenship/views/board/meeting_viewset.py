from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from citizenship.api.serializers.board import MeetingSerializer, AttendeeSerializer

from citizenship.models import Meeting

from citizenship.service.board import MeetingService


class MeetingViewSet(viewsets.ModelViewSet):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        meeting = MeetingService.create_meeting(
            title=serializer.validated_data['title'],
            board=serializer.validated_data['board'],
            date=serializer.validated_data['date'],
            time=serializer.validated_data['time'],
            location=serializer.validated_data['location'],
            agenda=serializer.validated_data['agenda'],
            status=serializer.validated_data['status']
        )
        return Response(MeetingSerializer(meeting).data, status=status.HTTP_201_CREATED)

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
        attendee = MeetingService.confirm_attendance(meeting.id, member_id)
        return Response(AttendeeSerializer(attendee).data, status=status.HTTP_200_OK)
