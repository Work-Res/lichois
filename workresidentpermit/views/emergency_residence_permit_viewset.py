from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from app.classes.application_summary import ApplicationSummary
from ..models import EmergencyResidencePermit
from ..api.serializers import EmergencyResidencePermitSerializer


def get_app_labels():
	return [
		'app_personal_details.Person',
		'app_address.ApplicationAddress',
		'app_contacts.Contact',
		'app_attachments.ApplicationAttachment',
		'app_passport.Passport',
		'app_emergency_residence_permit.EmergencyResidencePermit'
	]


class EmergencyResidencePermitViewSet(viewsets.ModelViewSet):
	queryset = EmergencyResidencePermit.objects.all()
	serializer_class = EmergencyResidencePermitSerializer
	
	@action(detail=False, methods=['get'], url_path='summary/(?P<document_number>[A-Za-z0-9-]+)',
	        url_name='emergency-summary')
	def summary(self, request, document_number):
		app_summary = ApplicationSummary(document_number, get_app_labels())
		return Response(data=app_summary.data())
