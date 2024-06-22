from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from app.classes.application_summary import ApplicationSummary
from ..models import EmergencyPermit
from ..api.serializers import EmergencyPermitSerializer


def get_app_labels():
	return [
		'workresidentpermit.EmergencyPermit'
	]


class EmergencyResidencePermitViewSet(viewsets.ModelViewSet):
	queryset = EmergencyPermit.objects.all()
	serializer_class = EmergencyPermitSerializer
	
	@action(detail=False, methods=['get'], url_path='summary/(?P<document_number>[A-Za-z0-9-]+)',
	        url_name='emergency-summary')
	def summary(self, request, document_number):
		app_summary = ApplicationSummary(document_number, get_app_labels())
		return Response(data=app_summary.data())