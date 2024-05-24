from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from app.api.common.web import APIMessage
from ..models import VotingProcess
from ..serializers import VotingProcessSerializer


class VotingProcessViewSet(viewsets.ModelViewSet):
	queryset = VotingProcess.objects.all()
	serializer_class = VotingProcessSerializer
	lookup_field = 'document_number'
	
	def create(self, request, *args, **kwargs):
		if request.user.is_chairperson():
			return super().create(request, *args, **kwargs)
		else:
			api_message = APIMessage(
				code=403,
				message="Forbidden",
				details="Only the chairperson can create a voting process.")
			raise PermissionDenied(api_message.to_dict())
