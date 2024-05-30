from rest_framework import viewsets
from rest_framework.response import Response

from ..models import AgendaItem
from ..serializers import AgendaItemSerializer


class AgendaItemViewSet(viewsets.ModelViewSet):
	queryset = AgendaItem.objects.all()
	serializer_class = AgendaItemSerializer
	
	def retrieve(self, request, agenda,  *args, **kwargs):
		queryset = AgendaItem.objects.filter(agenda__id=agenda)
		serializer = AgendaItemSerializer(queryset, many=True)
		return Response(serializer.data)
	
	def get_queryset(self):
		"""
		Optionally restricts the returned agenda items to a given agenda,
		by filtering against a `agenda` query parameter in the URL.
		"""
		agenda = self.request.query_params.get('agenda', None)
		if agenda is not None:
			queryset = AgendaItem.objects.filter(agenda__id=agenda)
		else:
			queryset = AgendaItem.objects.all()
		return queryset

