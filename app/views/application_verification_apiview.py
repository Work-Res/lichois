from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from app.api.serializers import ApplicationVerificationRequestSerializer
from app.api import ApplicationVerificationRequest
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
                    document_number=document_number, verification_request=verification_request)
                data = service.submit().result()
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response(validator.response.result(), status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
