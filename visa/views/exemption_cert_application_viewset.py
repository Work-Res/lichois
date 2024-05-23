from rest_framework import status, viewsets
from rest_framework.response import Response
from ..models import ExemptionCertificateApplication
from ..classes import ExemptionCertApplicationData
from ..serializers import VisaExemptionCertificateAppSerializer


class ExemptionCertificateApplicationViewSet(viewsets.ModelViewSet):
    queryset = ExemptionCertificateApplication.objects.all()
    serializer_class = VisaExemptionCertificateAppSerializer

    def retrieve(self, request, document_number, format=None):
        """
        Retrieve visa application details.
        """
        # document_number = request.query_params.get('document_number', None)

        if document_number is not None:
            exemption_cert_application_data = ExemptionCertApplicationData(document_number=document_number)
            if exemption_cert_application_data:
                print(exemption_cert_application_data.data().__dict__)
                serializer = VisaExemptionCertificateAppSerializer(exemption_cert_application_data.data())
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({})
