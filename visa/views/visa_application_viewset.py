from rest_framework import status, viewsets
from rest_framework.response import Response
from ..models import VisaApplication
from ..classes import VisaApplicationData
from ..serializers import VisaApplicationSerializer


class VisaApplicationViewSet(viewsets.ModelViewSet):
    queryset = VisaApplication.objects.all()
    serializer_class = VisaApplicationSerializer

    def retrieve(self, request, document_number, format=None):
        """
        Retrieve visa application details.
        """
        # document_number = request.query_params.get('document_number', None)

        if document_number is not None:
            visa_application_data = VisaApplicationData(document_number=document_number)
            if visa_application_data:
                print(visa_application_data.data().__dict__)
                serializer = VisaApplicationSerializer(visa_application_data.data())
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({})
