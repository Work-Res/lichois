from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from app.api.common.web import APIMessage
from ..models import BoardMember, MeetingInvitation
from ..serializers import MeetingInvitationSerializer


class MeetingInvitationViewSet(viewsets.ModelViewSet):
	serializer_class = MeetingInvitationSerializer
	queryset = MeetingInvitation.objects.all()
	
	def get_queryset(self):
		"""
        Optionally restricts the returned invitations to a given user,
        by filtering against a `invited_user` query parameter in the URL.
        """
		invited_user = self.request.user
		try:
			board_member = BoardMember.objects.get(user=invited_user)
		except BoardMember.DoesNotExist:
			api_message = APIMessage(
				code=400,
				message="Bad request",
				details="User is not a member of any board"
			)
			raise PermissionDenied(api_message.to_dict())
		else:
			self.queryset = MeetingInvitation.filter(invited_user=board_member)
		return self.queryset
