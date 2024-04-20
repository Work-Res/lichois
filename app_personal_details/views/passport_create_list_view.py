import logging

from rest_framework import generics, status

from rest_framework.response import Response

from ..models import Passport
from ..api.serializers import PassportSerializer

from ..classes import CreateNewPassport


class PassportCreateListView(generics.ListCreateAPIView):
    queryset = Passport.objects.all()
    serializer_class = PassportSerializer

    def post(self, request, document_number, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            passport_creater = CreateNewPassport(data=serializer.data)
            passport_creater.document_number = document_number
            passport_creater.create()
            if passport_creater.response.status:
                return Response(passport_creater.response.result(), status=status.HTTP_201_CREATED)
            else:
                return Response(passport_creater.response.result(), status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):  # filtering against query parameters
        document_number = self.request.query_params.get('document_number')
        passports = []
        if document_number:
            passport = Passport.objects.filter(
                application_version__application__application_document__document_number=document_number)
            passports.append(passport)
        return passports
