from rest_framework import serializers
from ..models import MeetingInvitation


class MeetingInvitationSerializer(serializers.ModelSerializer):
	class Meta:
		model = MeetingInvitation
		fields = ['id', 'meeting_title', 'invited_user', 'timestamp', 'status']
