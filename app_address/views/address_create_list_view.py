from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from ..models import ApplicationAddress
from ..api.serializers import ApplicationAddressSerializer

from ..classes import CreateApplicationAddress


class AddressCreateListView(viewsets.ModelViewSet):
    queryset = ApplicationAddress.objects.all()
    serializer_class = ApplicationAddressSerializer
    lookup_field = 'document_number'

    def post(self, request, document_number, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            address_application_creater = CreateApplicationAddress(data=serializer.data)
            address_application_creater.document_number = document_number
            address_application_creater.create()
            if address_application_creater.response.status:
                return Response(address_application_creater.response.result(), status=status.HTTP_201_CREATED)
            else:
                return Response(address_application_creater.response.result(), status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
