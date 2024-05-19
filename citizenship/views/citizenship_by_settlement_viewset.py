from rest_framework import viewsets
from ..models import CitizenshipBySettlement
from lichois.citizenship.api.serializers import CitizenshipBySettlementSerializer


class CitizenshipBySettlementViewSet(viewsets.ModelViewSet):
    queryset = CitizenshipBySettlement.objects.all()
    serializer_class = CitizenshipBySettlementSerializer

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
