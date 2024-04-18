import logging

from rest_framework import generics, status

from rest_framework.response import Response

from ..models import Person
from ..api import PersonSerializer

from app.models import ApplicationVersion


class PersonCreateListView(generics.ListCreateAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    def post(self, request, *args, **kwargs):
        logger = logging.getLogger(__name__)
        serializer = self.get_serializer(data=request.data)
        data = serializer.data
        document_number = data.get("application_number")
        if serializer.is_valid():
            try:
                try:
                    application_version = ApplicationVersion.objects.get(
                        application__application_document__document_number=document_number)
                    data = serializer.validated_data
                    data['application_version'] = application_version
                    del data['application_number']
                    Person.objects.create(**data)
                except ApplicationVersion.DoesNotExist:
                    logger.debug(f"Application Version with ID: {document_number} does not exists.")
            except Exception as e:
                logger.debug(f"Error while trying to create passport record {e}")
                pass
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        document_number = self.request.query_params.get('document_number')
        permits = []
        if document_number:
            person = Person.objects.filter(
                application_version__application__application_document__document_number=document_number)
            permits.append(person)
        return permits
