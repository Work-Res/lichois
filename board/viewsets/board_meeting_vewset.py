from rest_framework import status, viewsets
from rest_framework.response import Response

from ..models import BoardMeeting
from ..serializers import BoardMeetingSerializer


class BoardMeetingViewSet(viewsets.ModelViewSet):
	queryset = BoardMeeting.objects.all()
	serializer_class = BoardMeetingSerializer
	
	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save(request=request)
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	
	
