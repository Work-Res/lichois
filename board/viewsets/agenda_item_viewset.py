from rest_framework import viewsets
from rest_framework.response import Response

from ..models import AgendaItem
from ..serializers import AgendaItemSerializer


class AgendaItemViewSet(viewsets.ModelViewSet):
	queryset = AgendaItem.objects.all()
	serializer_class = AgendaItemSerializer
	lookup_field = 'agenda'
	
	def retrieve(self, request, agenda,  *args, **kwargs):
		queryset = AgendaItem.objects.filter(agenda__id=agenda)
		serializer = AgendaItemSerializer(queryset, many=True)
		return Response(serializer.data)

