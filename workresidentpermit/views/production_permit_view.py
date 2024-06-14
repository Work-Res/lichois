import os

from rest_framework import status

from rest_framework.views import APIView
from rest_framework.response import Response

from workresidentpermit.validators import ProductionValidator

from workresidentpermit.classes.production import FetchRequiredDataForProduction


class ProductionPermitView(APIView):

    def get(self, request, document_number):
        validator = ProductionValidator(document_number=document_number)
        if validator.is_valid():
            file_name = "work_resident_permit_only.json"
            configuration_file = os.path.join(
                os.getcwd(), "workresidentpermit", "classes", "production", "configuration", file_name)
            data_fetcher = FetchRequiredDataForProduction(
                configuration_file_name=configuration_file, document_number=document_number)
            return Response(data_fetcher.get_data(), status=status.HTTP_200_OK)
        else:
            return Response(validator.response.messages, status=status.HTTP_400_BAD_REQUEST)
