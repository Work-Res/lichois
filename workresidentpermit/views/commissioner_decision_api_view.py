from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
import logging

from rest_framework.views import APIView

from workresidentpermit.api.dto import RecommendationRequestDTO
from workresidentpermit.api.serializers import RecommendationRequestDTOSerializer
from workresidentpermit.classes.service.recommendation_service import RecommendationService

logger = logging.getLogger(__name__)


class CommissionerDecisionAPIView(APIView):
	"""
    Responsible for creating and retrieving a commissioner decision record.
    """
	def post(self, request, *args, **kwargs):
		try:
			serializer = RecommendationRequestDTOSerializer(data=request.data)
			if serializer.is_valid():
				data = serializer.validated_data
				request_dto = RecommendationRequestDTO(**data)
				service = RecommendationService(request_dto)
				return service.create_recommendation()
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		except Exception as e:
			logger.error(f"Unexpected error: {str(e)}", exc_info=True)
			return Response({'detail': f'Something went wrong. Got {str(e)}'},
			                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
	
	def get(self, request):
		document_number = request.query_params.get('document_number')
		if document_number:
			request_dto = RecommendationRequestDTO(document_number=document_number)
			service = RecommendationService(request_dto)
			return service.retrieve_recommendation()
		return Response({'detail': 'Document number is required'}, status=status.HTTP_400_BAD_REQUEST)
