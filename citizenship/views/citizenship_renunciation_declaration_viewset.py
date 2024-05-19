from rest_framework import status, viewsets
from rest_framework.response import Response
from ..models import CitizenshipRenunciationDeclaration
from ..classes import CitizenshipRenunciationDeclData
from lichois.citizenship.api.serializers import CitizenshipRenunciationDeclarationSerializer


class CitizenshipRenunciationDeclarationViewSet(viewsets.ModelViewSet):
    queryset = CitizenshipRenunciationDeclaration.objects.all()
    serializer_class = CitizenshipRenunciationDeclarationSerializer

    def retrieve(self, request, document_number, format=None):
        """
        Retrieve certificate of naturalisation by foreign spouse details.
        """
        # document_number = request.query_params.get('document_number', None)

        if document_number is not None:
            citizenship_renunciation_data = CitizenshipRenunciationDeclData(document_number=document_number)
            if citizenship_renunciation_data:
                print(citizenship_renunciation_data.data().__dict__)
                serializer = CitizenshipRenunciationDeclarationSerializer(citizenship_renunciation_data.data())
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({})

