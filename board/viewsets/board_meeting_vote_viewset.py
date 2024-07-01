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
	lookup_field = 'document_number'
	
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
			return Response(APIMessage(message='Tie breaker successfully created').to_dict(), status=201)
		return Response(APIMessage(message=f'Tie breaker failed to create {tiebreaker}', ).to_dict(), status=500)
	
	# get vote of current user logged in
	@action(detail=False, methods=['get'], url_path='my-vote/(?P<document_number>[A-Za-z0-9-]+)',
	        url_name='my-vote')
	def my_vote(self, request, document_number):
		meeting_vote_manager = self.get_meeting_vote_manager(request, document_number)
		vote = meeting_vote_manager.get_my_vote()
		if vote:
			return Response(data=BoardMeetingVoteSerializer(vote).data)
		return Response(APIMessage(message='Vote not found', code=404).to_dict(), status=404)
	
	def create(self, request, *args, **kwargs):
		# if vote exists, raise an error
		meeting_vote_manager = self.get_meeting_vote_manager(request, request.data.get('document_number'))
		if meeting_vote_manager.vote_exists():
			return Response(APIMessage(message='Vote already exists', code=500).to_dict(), status=500)
		return super().create(request, *args, **kwargs)
		
	@classmethod
	def get_meeting_vote_manager(cls, request, document_number):
		meeting_vote_manager = BoardMeetingVoteManager(
			user=request.user,
			document_number=document_number,
		)
		return meeting_vote_manager
