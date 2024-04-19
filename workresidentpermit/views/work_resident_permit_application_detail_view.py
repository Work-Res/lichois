from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from ..classes import WorkResidentPermitData
from ..api import WorkResidentPermitDataSerializer


class WorkResidentPermitApplicationDetailView(APIView):

    def get(self, request, document_number, format=None):
        """
        Retrieve work resident permit details.
        """
        # document_number = request.query_params.get('document_number', None)

        if document_number is not None:
            work_resident_permit_data = WorkResidentPermitData(document_number=document_number)
            if work_resident_permit_data:
                serializer = WorkResidentPermitDataSerializer(work_resident_permit_data.work_resident_permit_application)
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({})
