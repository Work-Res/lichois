from rest_framework import viewsets
from ..models import BoardMeetingVote
from ..serializers import BoardMeetingVoteSerializer


class BoardMeetingVoteViewSet(viewsets.ModelViewSet):
	queryset = BoardMeetingVote.objects.all()
	serializer_class = BoardMeetingVoteSerializer
