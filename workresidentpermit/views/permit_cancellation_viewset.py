from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from app.classes.application_summary import ApplicationSummary
from ..models import PermitCancellation
from ..api.serializers import PermitCancellationSerializer


def get_app_labels():
	return [
		'workresidentpermit.PermitCancellation',
		'workresidentpermit.CommissionerDecision',
		'workresidentpermit.MinisterDecision',
	]


class PermitCancellationViewSet(viewsets.ModelViewSet):
	queryset = PermitCancellation.objects.all()
	serializer_class = PermitCancellationSerializer
	
	@action(detail=False, methods=['get'], url_path='summary/(?P<document_number>[A-Za-z0-9-]+)',
	        url_name='cancellation-permit-summary')
	def summary(self, request, document_number):
		app_summary = ApplicationSummary(document_number, get_app_labels())
		return Response(data=app_summary.data())
