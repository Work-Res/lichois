import re

from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from citizenship.api.dto.citizenship_minister_decision_request_dto import \
    CitizenshipMinisterDecisionRequestDTOSerializer
from citizenship.api.dto.request_dto import CitizenshipMinisterRequestDTO
from citizenship.service.recommendation.citizenship_minister_decision_service import CitizenshipMinisterDecisionService


class CitizenshipMinisterDecisionAPIView(APIView):

    def post(self, request):
        try:
            serializer = CitizenshipMinisterDecisionRequestDTOSerializer(data=request.data)
            if serializer.is_valid():
                request = CitizenshipMinisterRequestDTO(**serializer.data)
                service = CitizenshipMinisterDecisionService(request)
                service.create_minister_decision()
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
        if document_number:
            request = CitizenshipMinisterRequestDTO(document_number=document_number)
            service = CitizenshipMinisterDecisionService(request)
            return service.retrieve_minister_decision()

        return Response(
            {"detail": "Document number is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )
