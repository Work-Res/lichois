from rest_framework import generics, status
from rest_framework import viewsets
from rest_framework.response import Response

from ..models import Person
from ..api import PersonSerializer

from ..classes import CreateNewPersonalDetails


class PersonCreateListView(viewsets.ModelViewSet):

    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    lookup_field = 'document_number'

    def post(self, request, document_number, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            person_creater = CreateNewPersonalDetails(data=serializer.data)
            person_creater.document_number = document_number
            person_creater.create()
            if person_creater.response.status:
                return Response(person_creater.response.result(), status=status.HTTP_201_CREATED)
            else:
                return Response(person_creater.response.result(), status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
