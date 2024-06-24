from rest_framework import viewsets
from rest_framework.response import Response

from ..models import Agenda
from ..serializers import AgendaSerializer


class AgendaViewSet(viewsets.ModelViewSet):
	queryset = Agenda.objects.all()
	serializer_class = AgendaSerializer
	lookup_field = 'meeting'

	def retrieve(self, request, meeting,  *args, **kwargs):
		# Filter by meeting
		queryset = Agenda.objects.filter(meeting__id=meeting)
		serializer = AgendaSerializer(queryset, many=True)
		return Response(serializer.data)
