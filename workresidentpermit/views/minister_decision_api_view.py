from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from workresidentpermit.api.dto import MinisterRequestDTO
from workresidentpermit.api.serializers import MinisterDecisionRequestDTOSerializer
from workresidentpermit.classes.service import MinisterDecisionService


class MinisterDecisionAPIView(APIView):
	def post(self, request):
		try:
			serializer = MinisterDecisionRequestDTOSerializer(request.data)
			if serializer.is_valid():
				request = MinisterRequestDTO(**serializer.data)
				service = MinisterDecisionService(request)
				return service.create_minister_decision()
		except Exception as e:
			return Response({'detail': f'Something went wrong. Got {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
		
	def get(self, request, document_number=None):
		if document_number:
			request = MinisterRequestDTO(document_number=document_number)
			service = MinisterDecisionService(request)
			return service.retrieve_minister_decision()
		
		return Response({'detail': 'Document number is required'}, status=status.HTTP_400_BAD_REQUEST)
