import re
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.api.common.web.api_error import APIMessage
from app.api.dto.application_verification_request_dto import (
    ApplicationVerificationRequestDTO,
)
from app.api.serializers import (
    ApplicationVerificationRequestSerializer,
    ApplicationVerificationSerializer,
)
from app.models.application_verification import ApplicationVerification
from app.service import VerificationService
from app.validators import OfficerVerificationValidator


class ApplicationVerificationAPIView(APIView):

    def post(self, request, document_number):
        serializer = ApplicationVerificationRequestSerializer(data=request.data)
        if serializer.is_valid():
            validator = OfficerVerificationValidator(document_number=document_number)
            if validator.is_valid():
                verification_request = ApplicationVerificationRequestDTO(
                    document_number=document_number,
                    user=request.user,
                    **serializer.data
                )
                service = VerificationService(verification_request=verification_request)
                data = service.create_verification()
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response(
                    validator.response.result(), status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, document_number):
        # get the application verification using the document number
        verification_request = ApplicationVerificationRequestDTO(
            document_number=document_number
        )
        service = VerificationService(verification_request=verification_request)
        return service.retrieve_verification()
