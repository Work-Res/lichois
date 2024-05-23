from rest_framework import serializers
from ..models import MeetingInvitation


class MeetingInvitationSerializer(serializers.ModelSerializer):
	class Meta:
		model = MeetingInvitation
		fields = [
			'id',
			'timestamp',
			'status',
			'board_meeting'
		]
