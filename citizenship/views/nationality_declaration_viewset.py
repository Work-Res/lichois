from rest_framework import status, viewsets
from rest_framework.response import Response
from ..models import NationalityDeclaration
from ..classes import NationalityDeclarationData
from lichois.citizenship.api.serializers import NationalityDeclarationSerializer


class NationalityDeclarationViewSet(viewsets.ModelViewSet):
    queryset = NationalityDeclaration.objects.all()
    serializer_class = NationalityDeclarationSerializer

    def retrieve(self, request, document_number, format=None):
        """
        Retrieve nationality declaration details.
        """
        # document_number = request.query_params.get('document_number', None)

        if document_number is not None:
            nationality_declaration_data = NationalityDeclarationData(document_number=document_number)
            if nationality_declaration_data:
                print(nationality_declaration_data.data().__dict__)
                serializer = NationalityDeclarationSerializer(nationality_declaration_data.data())
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({})

