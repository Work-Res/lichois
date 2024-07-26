import re

from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..api.dto import MinisterRequestDTO
from ..api.serializers import MinisterDecisionRequestDTOSerializer
from ..service import MinisterDecisionService


class MinisterDecisionAPIView(APIView):

    def post(self, request):
        try:
            serializer = MinisterDecisionRequestDTOSerializer(data=request.data)
            if serializer.is_valid():
                request = MinisterRequestDTO(**serializer.data)
                service = MinisterDecisionService(request)
                service.create_minister_decision()
                service.response.result()
            return JsonResponse(service.response.result())
        except Exception as e:
            return JsonResponse(
                {"error": "Invalid JSON in request body"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def get(self, request):
        document_number = request.query_params.get("document_number")
        if document_number:
            request = MinisterRequestDTO(document_number=document_number)
            service = MinisterDecisionService(request)
            return service.retrieve_minister_decision()

        return Response(
            {"detail": "Document number is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )
