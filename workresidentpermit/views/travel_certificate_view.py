import os

from rest_framework import status

from rest_framework.views import APIView
from rest_framework.response import Response

from app_production.validators import ProductionValidator

from app_production.classes import PermitDataProcessor


class TravelCertificateView(APIView):

    def get(self, request, document_number):
        validator = ProductionValidator(document_number=document_number)
        if validator.is_valid():
            file_name = "travel_certificate.json"
            configuration_file = os.path.join(
                os.getcwd(),
                "workresidentpermit",
                "classes",
                "production",
                "configuration",
                file_name,
            )
            permit_data = PermitDataProcessor(
                configuration_file_name=configuration_file,
                document_number=document_number,
            )
            return Response(permit_data.transform_data(), status=status.HTTP_200_OK)
        else:
            return Response(
                validator.response.messages, status=status.HTTP_400_BAD_REQUEST
            )
