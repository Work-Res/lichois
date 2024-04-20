from rest_framework import viewsets

from rest_framework import status

from rest_framework.response import Response

from ..models import ApplicationContact
from ..api.serializers import ApplicationContactSerializer

from ..classes import CreateNewApplicationContact


class ApplicationContactViewSet(viewsets.ModelViewSet):
    queryset = ApplicationContact.objects.all()
    serializer_class = ApplicationContactSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            contact_creater = CreateNewApplicationContact(data=serializer.data)
            contact_creater.create()
            if contact_creater.response.status:
                return Response(contact_creater.response.result(), status=status.HTTP_201_CREATED)
            else:
                return Response(contact_creater.response.result(), status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

