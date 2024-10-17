import re

from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from citizenship.api.dto import ForeignRenunciationRequestDTO
from citizenship.api.dto.citizenship_minister_decision_request_dto import ForeignRenunciationDecisionSerializer

from citizenship.service.foreign_renunciation.foreign_renunciation_decision_service import (
    ForeignRenunciationDecisionService)


class CitizenshipForeignRenunciationDecisionAPIView(APIView):

    def post(self, request):
        try:
            serializer = ForeignRenunciationDecisionSerializer(data=request.data)
            if serializer.is_valid():
                request = ForeignRenunciationRequestDTO(**serializer.data)
                request.comment_type = "foreign_renunciation_decision"
                service = ForeignRenunciationDecisionService(request)
                service.create_foreign_renunciation_decision()
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
            request = ForeignRenunciationRequestDTO(document_number=document_number)
            service = ForeignRenunciationDecisionService(request)
            return Response(service.retrieve_foreign_renunciation_decision(), status=status.HTTP_200_OK)

        return Response(
            {"detail": "Document number is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )
