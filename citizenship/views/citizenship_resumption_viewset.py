from rest_framework import status, viewsets
from rest_framework.response import Response
from ..models import CitizenshipResumption
from ..classes import CitizenshipResumptionData
from lichois.citizenship.api.serializers import CitizenshipResumptionSerializer


class CitizenshipResumptionViewSet(viewsets.ModelViewSet):
    queryset = CitizenshipResumption.objects.all()
    serializer_class = CitizenshipResumptionSerializer

    def retrieve(self, request, document_number, format=None):
        """
        Retrieve certificate of naturalisation by foreign spouse details.
        """
        # document_number = request.query_params.get('document_number', None)

        if document_number is not None:
            citizenship_resumption_data = CitizenshipResumptionData(document_number=document_number)
            if citizenship_resumption_data:
                print(citizenship_resumption_data.data().__dict__)
                serializer = CitizenshipResumptionSerializer(citizenship_resumption_data.data())
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({})

