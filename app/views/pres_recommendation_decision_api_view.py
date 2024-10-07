from django.http import JsonResponse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..api.dto import PresRecommendationRequestDTO
from ..api.serializers import PresRecommendationDecisionSerializer
from ..models import PresRecommendationDecision
from ..service.pres_recommendation_decision import PresRecommendationDecisionService


class PresRecommendationDecisionAPIView(APIView):

    def post(self, request):
        try:
            serializer = PresRecommendationDecisionSerializer(data=request.data)
            if serializer.is_valid():
                request = PresRecommendationRequestDTO(**serializer.data)
                service = PresRecommendationDecisionService(request)
                service.create_decision(PresRecommendationDecision, PresRecommendationDecisionSerializer)
                service.response.result()
                return JsonResponse(service.response.result())
            else:
                return JsonResponse(
                    {"error": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as ex:
            return JsonResponse(
                {"error": f"Invalid JSON in request body {ex}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def get(self, request):
        document_number = request.query_params.get("document_number")
        role = request.query_params.get("role")

        if document_number:
            request = PresRecommendationRequestDTO(document_number=document_number, role=role)
            service = PresRecommendationDecisionService(request)
            return service.retrieve_decision(PresRecommendationDecision, PresRecommendationDecisionSerializer)

        return Response(
            {"detail": "Document number is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

