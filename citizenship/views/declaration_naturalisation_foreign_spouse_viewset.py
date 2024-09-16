from rest_framework import status, viewsets
from rest_framework.response import Response
from ..models import DeclarationNaturalisationByForeignSpouse
from ..classes import DeclNaturalisationForeignSpouseData

from citizenship.api.serializers import DeclNaturalisationForeignSpouseSerializer


class DeclarationNaturalisationForeignSpouseViewSet(viewsets.ModelViewSet):
    queryset = DeclarationNaturalisationByForeignSpouse.objects.all()
    serializer_class = DeclNaturalisationForeignSpouseSerializer

    def retrieve(self, request, document_number, format=None):
        """
        Retrieve declaratgion of intent of naturalisation by foreign spouse details.
        """
        # document_number = request.query_params.get('document_number', None)

        if document_number is not None:
            declaration_intent_naturalisation_data = DeclNaturalisationForeignSpouseData(document_number=document_number)
            if declaration_intent_naturalisation_data:
                print(declaration_intent_naturalisation_data.data().__dict__)
                serializer = DeclNaturalisationForeignSpouseSerializer(declaration_intent_naturalisation_data.data())
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({})
