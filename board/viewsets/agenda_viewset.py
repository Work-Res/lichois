from rest_framework import viewsets
from ..models import Agenda
from ..serializers import AgendaSerializer


class AgendaViewSet(viewsets.ModelViewSet):
	queryset = Agenda.objects.all()
	serializer_class = AgendaSerializer


def get_queryset(self):
	# Filter by meeting
	return self.queryset.filter(meeting__id=self.kwargs['meeting'])
