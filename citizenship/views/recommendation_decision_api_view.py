from django.http import JsonResponse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.api.serializers import (
    RecommendationRequestDTOSerializer,
)

from citizenship.api.dto import RecommendationDecisionRequestDTO
from citizenship.service.recommendation import RecommendationDecisionService


class RecommendationDecisionAPIView(APIView):

    def post(self, request):
        try:
            serializer = RecommendationRequestDTOSerializer(data=request.data)
            if serializer.is_valid():
                data = serializer.validated_data
                data.update({
                    "user": request.user
                })
                request_dto = RecommendationDecisionRequestDTO(
                    **data,
                )
                service = RecommendationDecisionService(decision_request=request_dto)
                return Response(
                    service.create_recommendation(), status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as ex:
            return JsonResponse(
                {"error": f"Invalid JSON in request body {ex}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def get(self, request):
        document_number = request.query_params.get("document_number")
        if document_number:
            request = RecommendationRequestDTOSerializer(document_number=document_number)
            service = RecommendationDecisionService(request)
            return service.retrieve_recommendation()

        return Response(
            {"detail": "Document number is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )
