from rest_framework import mixins, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
import logging

from workresidentpermit.api.dto import RecommendationRequestDTO
from workresidentpermit.api.serializers import RecommendationRequestDTOSerializer
from workresidentpermit.classes.service.recommendation_service import RecommendationService

logger = logging.getLogger(__name__)

class CommissionerDecisionAPIView(mixins.CreateModelMixin, mixins.RetrieveModelMixin, GenericAPIView):
    """
    Responsible for creating a commissioner decision record.
    POST
        {
            "document_number": "document_number",
            "status": "pending", # list of valid options ['pending', 'Rejected', 'Accepted'],
            "summary": "text"
        }
    """
    serializer_class = RecommendationRequestDTOSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
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

    def get(self, request, *args, **kwargs):
        document_number = kwargs.get('document_number')
        if document_number:
            return self.retrieve(request, document_number, *args, **kwargs)
        return Response({'detail': 'Document number is required'}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, document_number, *args, **kwargs):
        request_dto = RecommendationRequestDTO(document_number=document_number)
        service = RecommendationService(request_dto)
        return service.retrieve_recommendation()
