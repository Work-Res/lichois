from django.views.generic import View
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from workresidentpermit.api.dto import MinisterRequestDTO
from workresidentpermit.api.serializers import MinisterDecisionRequestDTOSerializer
from workresidentpermit.classes.service import MinisterDecisionService


class MinisterDecisionViewView(viewsets.ViewSet):
	def post(self, request):
		try:
			serializer = MinisterDecisionRequestDTOSerializer(request.data)
			if serializer.is_valid():
				request = MinisterRequestDTO(**serializer.data)
				service = MinisterDecisionService(request)
				return service.create_minister_decision()
		except Exception as e:
			return Response({'detail': f'Something went wrong. Got {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
		
	@action(detail=False, methods=['get'], url_path='(?P<document_number>[A-Za-z0-9-]+)',
	        url_name='minister-decision-detail')
	def get_minister_decision(self, request, document_number=None):
		if document_number:
			request = MinisterRequestDTO(document_number=document_number)
			service = MinisterDecisionService(request)
			return service.retrieve_minister_decision()
		
		return Response({'detail': 'Document number is required'}, status=status.HTTP_400_BAD_REQUEST)
