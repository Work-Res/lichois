from rest_framework import serializers
from ..models import BoardMeeting


class BoardMeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardMeeting
        fields = '__all__'
