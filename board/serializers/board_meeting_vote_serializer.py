from rest_framework import serializers
from ..models import BoardMeetingVote


class BoardMeetingVoteSerializer(serializers.ModelSerializer):
	class Meta:
		model = BoardMeetingVote
		fields = '__all__'
