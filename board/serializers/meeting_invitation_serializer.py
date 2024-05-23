from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from app.api.common.web import APIMessage
from . import BoardMemberSerializer
from ..models import BoardMember, MeetingInvitation


class MeetingInvitationSerializer(serializers.ModelSerializer):
	invited_user = BoardMemberSerializer(required=False)
	
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
		if not board_member:
			api_message = APIMessage(
				code=400,
				message="Bad request",
				details="User is not a member of any board"
			)
			raise PermissionDenied(api_message.to_dict())
		mutable_data['invited_user'] = board_member.id
		return super().to_internal_value(mutable_data)
