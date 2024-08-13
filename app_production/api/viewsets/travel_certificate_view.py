import re
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ...api.dto.permit_request_dto import PermitRequestDTO
from ...services.travel_certificate_production_service import (
    TravelCertificateProductionService,
)


class TravelCertificateProductionPermitView(APIView):

    def get(self, request, document_number):
        try:
            request = PermitRequestDTO()
            request.document_number = document_number
            service = TravelCertificateProductionService(request)
            context_data = service.get_context_data()
            return Response(data=context_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
