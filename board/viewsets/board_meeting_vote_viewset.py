from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import BoardMeetingVote
from ..serializers import BoardMeetingVoteSerializer
from ..classes import BoardMeetingVoteManager


class BoardMeetingVoteViewSet(viewsets.ModelViewSet):
	queryset = BoardMeetingVote.objects.all()
	serializer_class = BoardMeetingVoteSerializer
	
	@action(detail=False, methods=['get'])
	def voted_members(self, request):
		meeting_vote_manager = BoardMeetingVoteManager(user=request.user)   # Instantiate the BoardMeetingVoteManager class
		votes = meeting_vote_manager.get_votes()  # Get the votes
		return Response(votes)
