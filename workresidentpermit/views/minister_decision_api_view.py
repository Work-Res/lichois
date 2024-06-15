from django.views.generic import View
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from workresidentpermit.api.dto import MinisterRequestDTO
from workresidentpermit.api.serializers import MinisterDecisionRequestDTOSerializer
from workresidentpermit.classes.service import MinisterDecisionService


class MinisterDecisionAPIView(APIView):
	
	def post(self, request):
		try:
			serializer = MinisterDecisionRequestDTOSerializer(data=request.data)
			if serializer.is_valid():
				request = MinisterRequestDTO(**serializer.data)
				service = MinisterDecisionService(request)
				return service.create_minister_decision()
		except Exception as e:
			return Response({'detail': f'Something went wrong. Got {str(e)}'},
			                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
	
	def get(self, request, *args, **kwargs):
		document_number = kwargs.get('document_number')
		if document_number:
			request = MinisterRequestDTO(document_number=document_number)
			service = MinisterDecisionService(request)
			return service.retrieve_minister_decision()
		
		return Response({'detail': 'Document number is required'}, status=status.HTTP_400_BAD_REQUEST)
