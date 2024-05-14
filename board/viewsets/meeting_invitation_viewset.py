from rest_framework import viewsets
from ..models import MeetingInvitation
from ..serializers import MeetingInvitationSerializer


class MeetingInvitationViewSet(viewsets.ModelViewSet):
	serializer_class = MeetingInvitationSerializer
	
	def get_queryset(self):
		"""
        Optionally restricts the returned invitations to a given user,
        by filtering against a `invited_user` query parameter in the URL.
        """
		queryset = MeetingInvitation.objects.all()
		invited_user = self.request.query_params.get('invited_user', None)
		if invited_user is not None:
			queryset = queryset.filter(invited_user__id=invited_user)
		return queryset
