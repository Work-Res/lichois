from rest_framework import status, viewsets
from rest_framework.response import Response
from ..models import RenunciationOfForeignCitizenship
from ..classes import RenunciationOfForeignCitizenshipData
from lichois.citizenship.api.serializers import RenunciationOfForeignCitizenshipSerializer


class RenunciationOfForeignCitizenshipViewSet(viewsets.ModelViewSet):
    queryset = RenunciationOfForeignCitizenship.objects.all()
    serializer_class = RenunciationOfForeignCitizenshipSerializer

    def retrieve(self, request, document_number, format=None):
        """
        Retrieve certificate of naturalisation by foreign spouse details.
        """
        # document_number = request.query_params.get('document_number', None)

        if document_number is not None:
            renunciation_foreign_citizenship_data = RenunciationOfForeignCitizenshipData(document_number=document_number)
            if renunciation_foreign_citizenship_data:
                print(renunciation_foreign_citizenship_data.data().__dict__)
                serializer = RenunciationOfForeignCitizenshipSerializer(renunciation_foreign_citizenship_data.data())
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({})

