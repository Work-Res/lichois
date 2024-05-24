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
	
	@action(detail=False, methods=['get'], url_path='participants/(?P<document_number>[A-Za-z0-9-]+)',
	        url_name='participants')
	def voted_members(self, request, document_number):
		meeting_vote_manager = self.get_meeting_vote_manager(request, document_number)
		votes = meeting_vote_manager.get_votes()  # Get the votes
		return Response(data=votes)
	
	@action(detail=False, methods=['POST'], url_path='tie-breaker/(?P<document_number>[A-Za-z0-9-]+)',
	        url_name='tie-breaker')
	def create_tie_breaker(self, request, document_number):
		meeting_vote_manager = self.get_meeting_vote_manager(request, document_number)
		tie_breaker = request.POST.get('tie_breaker')
		tiebreaker = meeting_vote_manager.create_tie_breaker(tie_breaker)
		if tiebreaker:
			return Response(APIMessage(message='Tie breaker successfully created').to_dict())
		raise Exception(APIMessage(message='Tie breaker failed to create').to_dict())
	
	@classmethod
	def get_meeting_vote_manager(cls, request, document_number):
		meeting_vote_manager = BoardMeetingVoteManager(
			user=request.user,
			document_number=document_number,
		)
		return meeting_vote_manager
