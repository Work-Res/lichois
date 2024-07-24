import re
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.api import ApplicationVerificationRequest
from app.api.common.web.api_error import APIMessage
from app.api.serializers import (
    ApplicationVerificationRequestSerializer,
    ApplicationVerificationSerializer,
)
from app.models.application_verification import ApplicationVerification
from app.service import OfficerVerificationService
from app.validators import OfficerVerificationValidator


class ApplicationVerificationAPIView(APIView):

    def post(self, request, document_number):
        serializer = ApplicationVerificationRequestSerializer(data=request.data)
        if serializer.is_valid():
            validator = OfficerVerificationValidator(document_number=document_number)
            if validator.is_valid():
                verification_request = ApplicationVerificationRequest(**serializer.data)
                service = OfficerVerificationService(
                    document_number=document_number,
                    verification_request=verification_request,
                )
                data = service.submit().result()
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response(
                    validator.response.result(), status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, document_number):
        # get the application verification using the document number
        try:
            verification = ApplicationVerification.objects.get(
                document_number=document_number
            )
        except ApplicationVerification.DoesNotExist:
            return Response(
                APIMessage(
                    details=f"Application verification with document number {document_number} does not exist",
                    code=status.HTTP_404_NOT_FOUND,
                    message="Not Found",
                ).to_dict(),
                status=status.HTTP_404_NOT_FOUND,
            )
        else:
            serializer = ApplicationVerificationSerializer(verification)
            return Response(serializer.data, status=status.HTTP_200_OK)
