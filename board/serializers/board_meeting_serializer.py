from rest_framework import serializers, status
from rest_framework.response import Response

from app.api.common.web import APIMessage
from ..models import BoardMeeting, BoardMember


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
			'board',
		)
	
	# def create(self, validated_data):
	# 	request = self.context.get('request')
	# 	auth_user = request.user
	# 	board = BoardMember.objects.filter(user=auth_user).first().board
	# 	if not board:
	# 		api_message = APIMessage(
	# 			code=400,
	# 			message="Bad request",
	# 			details="User is not a member of any board"
	# 		)
	# 		return Response(data=api_message.to_dict(), status=status.HTTP_400_BAD_REQUEST)
	# 	validated_data['board'] = board
	# 	return super().create(validated_data)
