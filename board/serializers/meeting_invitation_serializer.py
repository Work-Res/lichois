from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from app.api.common.web import APIMessage
from . import BoardMeetingSerializer, BoardMemberSerializer
from ..models import BoardMeeting, BoardMember, MeetingInvitation


class MeetingInvitationSerializer(serializers.ModelSerializer):
	board_meeting = BoardMeetingSerializer()
	
	class Meta:
		model = MeetingInvitation
		fields = [
			'id',
			'timestamp',
			'status',
			'board_meeting',
			'invited_user',
		]
	
	def to_internal_value(self, data):
		request = self.context.get('request')
		auth_user = request.user
		mutable_data = data.copy()
		board_member = BoardMember.objects.filter(user=auth_user).first()
		board_meeting = BoardMeeting.objects.filter(id=data.get('board_meeting')).first()
		if not board_member:
			api_message = APIMessage(
				code=400,
				message="Bad request",
				details="User is not a member of any board"
			)
			raise PermissionDenied(api_message.to_dict())
		mutable_data['invited_user'] = board_member.id
		mutable_data['board_meeting'] = board_meeting
		return super().to_internal_value(mutable_data)
