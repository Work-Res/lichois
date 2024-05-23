from rest_framework import status, viewsets
from rest_framework.response import Response
from ..models import LateCitizenshipRenunciation
from ..classes import LateCitizenshipRenunciationData
from lichois.citizenship.api.serializers import LateCitizenshipRenunciationSerializer


class LateCitizenshipRenunciationViewSet(viewsets.ModelViewSet):
    queryset = LateCitizenshipRenunciation.objects.all()
    serializer_class = LateCitizenshipRenunciationSerializer

    def retrieve(self, request, document_number, format=None):
        """
        Retrieve certificate of naturalisation by foreign spouse details.
        """
        # document_number = request.query_params.get('document_number', None)

        if document_number is not None:
            late_citizenship_renunciation_data = LateCitizenshipRenunciationData(document_number=document_number)
            if late_citizenship_renunciation_data:
                print(late_citizenship_renunciation_data.data().__dict__)
                serializer = LateCitizenshipRenunciationSerializer(late_citizenship_renunciation_data.data())
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({})

