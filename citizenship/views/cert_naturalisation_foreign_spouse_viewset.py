from rest_framework import status, viewsets
from rest_framework.response import Response
from ..models import CertNaturalisationByForeignSpouse
from ..classes import CertNaturalisationForeignSpouseData
from ..api.serializers import CertNaturalisationByForeignSpouseSerializer


class CertNaturalisationByForeignSpouseViewSet(viewsets.ModelViewSet):
    queryset = CertNaturalisationByForeignSpouse.objects.all()
    serializer_class = CertNaturalisationByForeignSpouseSerializer

    def retrieve(self, request, document_number, format=None):
        """
        Retrieve certificate of naturalisation by foreign spouse details.
        """
        # document_number = request.query_params.get('document_number', None)

        if document_number is not None:
            cert_declaration_naturalisation_data = CertNaturalisationForeignSpouseData(document_number=document_number)
            if cert_declaration_naturalisation_data:
                print(cert_declaration_naturalisation_data.data().__dict__)
                serializer = CertNaturalisationByForeignSpouseSerializer(cert_declaration_naturalisation_data.data())
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({})
