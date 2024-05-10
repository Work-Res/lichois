from rest_framework import viewsets
from ..models import Agenda
from ..serializers import AgendaSerializer


class AgendaViewSet(viewsets.ModelViewSet):
	queryset = Agenda.objects.all()
	serializer_class = AgendaSerializer


def get_queryset(self):
	# Filter by meeting
	meeting = self.kwargs.get('meeting')
	queryset = super().get_queryset()
	user = self.request.user
	if user.is_superuser:
		return queryset
	return queryset.filter(meeting__id=meeting)
