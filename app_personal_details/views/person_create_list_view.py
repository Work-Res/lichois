from rest_framework import generics, status

from rest_framework.response import Response

from ..models import Person
from ..api import PersonSerializer

from ..classes import CreateNewPersonalDetails


class PersonCreateListView(generics.ListCreateAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

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

    def get_queryset(self):
        document_number = self.request.query_params.get('document_number')
        permits = []
        if document_number:
            person = Person.objects.filter(
                application_version__application__application_document__document_number=document_number)
            permits.append(person)
        return permits
