from rest_framework import serializers
from ..models import MeetingAttendee


class MeetingAttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingAttendee
        fields = '__all__'
