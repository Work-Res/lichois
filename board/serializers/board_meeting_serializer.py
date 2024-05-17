from rest_framework import serializers
from ..models import BoardMeeting


class BoardMeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardMeeting
        fields = (
            'id',
            'title',
            'meeting_date',
            'description',
            'status',
            'minutes',
            'meeting_type',
            'location',
        )
