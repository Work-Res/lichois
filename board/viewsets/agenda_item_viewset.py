from rest_framework import viewsets
from ..models import AgendaItem
from ..serializers import AgendaItemSerializer


class AgendaItemViewSet(viewsets.ModelViewSet):
	queryset = AgendaItem.objects.all()
	serializer_class = AgendaItemSerializer
	
	def get_queryset(self):
		return self.queryset.filter(agenda__id=self.kwargs['agenda'])

