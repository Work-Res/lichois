import json

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from app.api.common.web import APIMessage
from ..models import BoardMeetingVote
from ..serializers import BoardMeetingVoteSerializer
from ..classes import BoardMeetingVoteManager


class BoardMeetingVoteViewSet(viewsets.ModelViewSet):
	queryset = BoardMeetingVote.objects.all()
	serializer_class = BoardMeetingVoteSerializer
	
	@action(detail=False, methods=['get'])
	def voted_members(self, request):
		meeting_vote_manager = BoardMeetingVoteManager(
			user=request.user)  # Instantiate the BoardMeetingVoteManager class
		votes = meeting_vote_manager.get_votes()  # Get the votes
		return Response(data=votes)
	
	@action(detail=False, methods=['POST'], url_path='tie-breaker', url_name='tie-breaker')
	def create_tie_breaker(self, request):
		meeting_vote_manager = BoardMeetingVoteManager(
			user=request.user)
		tie_breaker = request.POST.get('tie_breaker')
		document_number = request.POST.get('document_number')
		tiebreaker = meeting_vote_manager.create_tie_breaker(document_number, tie_breaker)
		if tiebreaker:
			return Response(APIMessage(message='Tiebreaker successfully created').to_dict())
		raise Exception(APIMessage(message='Tiebreaker failed to create').to_dict())
		
