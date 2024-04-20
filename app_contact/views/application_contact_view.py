from rest_framework import viewsets

from rest_framework import status

from rest_framework.response import Response

from ..models import ApplicationContact
from ..api.serializers import ApplicationContactSerializer

from ..classes import CreateNewApplicationContact


class ApplicationContactViewSet(viewsets.ModelViewSet):
    queryset = ApplicationContact.objects.all()
    serializer_class = ApplicationContactSerializer
    lookup_field = 'document_number'

    def post(self, request, document_number, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            contact_creater = CreateNewApplicationContact(data=serializer.data)
            contact_creater.document_number = document_number
            contact_creater.create()
            if contact_creater.response.status:
                return Response(contact_creater.response.result(), status=status.HTTP_201_CREATED)
            else:
                return Response(contact_creater.response.result(), status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, document_number, *args, **kwargs):
        contacts = ApplicationContact.objects.filter(document_number=document_number)
        serializer = ApplicationContactSerializer(contacts, many=True)
        return Response(serializer.data)

    def update_contact(self, request, document_number=None, pk=None, custom_param=None):
        # Retrieve the instance based on pk
        instance = ApplicationContact.objects.get(id=pk, document_number=document_number)
        # Update the instance with the provided data
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
