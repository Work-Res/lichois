import logging

from rest_framework import generics, status

from rest_framework.response import Response

from ..models import Passport
from ..api.serializers import PassportSerializer

from app.models import ApplicationVersion


class PassportCreateListView(generics.ListCreateAPIView):
    queryset = Passport.objects.all()
    serializer_class = PassportSerializer

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
                    Passport.objects.create(**data)
                except ApplicationVersion.DoesNotExist:
                    logger.debug(f"Application Version with ID: {document_number} does not exists.")
            except Exception as e:
                logger.debug(f"Error while trying to create passport record {e}")
                pass
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):  # filtering against query parameters
        document_number = self.request.query_params.get('document_number')
        passports = []
        if document_number:
            passport = Passport.objects.filter(
                application_version__application__application_document__document_number=document_number)
            passports.append(passport)
        return passports
