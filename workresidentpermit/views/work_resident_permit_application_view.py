from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..validators import WorkResidentPermitValidator
from ..classes import WorkResidentPermitApplication


class WorkResidentPermitApplicaitonAPIView(APIView):

    def post(self, request, document_number):
        validator = WorkResidentPermitValidator(document_number=document_number)
        if validator.is_valid():
            application = WorkResidentPermitApplication(document_number=document_number)
            response = application.submit().result()
            return Response(response.result(), status=status.HTTP_200_OK)
        else:
            return Response(validator.response.result(), status=status.HTTP_400_BAD_REQUEST)
