from rest_framework import status, viewsets
from rest_framework.response import Response
from ..models import BlueCardApplication
from ..classes import BlueCardApplicationData
from ..serializers import BlueCardApplicationSerializer


class BlueCardApplicationViewSet(viewsets.ModelViewSet):
    queryset = BlueCardApplication.objects.all()
    serializer_class = BlueCardApplicationSerializer

    def retrieve(self, request, document_number, format=None):
        """
        Retrieve visa application details.
        """
        # document_number = request.query_params.get('document_number', None)

        if document_number is not None:
            blue_card_application_data = BlueCardApplicationData(document_number=document_number)
            if blue_card_application_data:
                print(blue_card_application_data.data().__dict__)
                serializer = BlueCardApplicationData(blue_card_application_data.data())
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({})

