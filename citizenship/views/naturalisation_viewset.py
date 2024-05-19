from rest_framework import status, viewsets
from rest_framework.response import Response
from ..models import Naturalisation
from ..classes import NaturalisationData
from lichois.citizenship.api.serializers import NaturalisationSerializer


class NaturalisationViewSet(viewsets.ModelViewSet):
    queryset = Naturalisation.objects.all()
    serializer_class = NaturalisationSerializer

    def retrieve(self, request, document_number, format=None):
        """
        Retrieve certificate of naturalisation by foreign spouse details.
        """
        # document_number = request.query_params.get('document_number', None)

        if document_number is not None:
            naturalisation_data = NaturalisationData(document_number=document_number)
            if naturalisation_data:
                print(naturalisation_data.data().__dict__)
                serializer = NaturalisationSerializer(naturalisation_data.data())
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({})

