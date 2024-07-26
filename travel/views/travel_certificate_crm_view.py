import os
import logging
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers import TravelCertificateSerializer
from app_personal_details.models import Person
from app_address.models import ApplicationAddress
from ..models import TravelCertificate, ApplicantRelative
from ..validators import TravelCertificateValidator
from workresidentpermit.classes.production import PermitDataProcessor

class TravelCertificateCrmView(APIView):
    
    def post(self, request):
        serializer = TravelCertificateSerializer(data=request.data)
        if serializer.is_valid():
            travel_certificate = serializer.save()
            document_number = travel_certificate.document_number

            model_classes = {
                'app_personal_details_Person': Person,
                'app_address_ApplicationAddress': ApplicationAddress,
                'travel_TravelCertificate': TravelCertificate,
                'travel_ApplicantRelative': ApplicantRelative
            }
            
            instances = {key: model() for key, model in model_classes.items()}
            instances['travel_TravelCertificate'] = travel_certificate

            for key, value in request.data.items():
                parts = key.split('_')
                if len(parts) >= 3:
                    model_key = f"{parts[0]}_{parts[1]}"
                    field_name = '_'.join(parts[2:])
                    if model_key in instances and hasattr(instances[model_key], field_name):
                        setattr(instances[model_key], field_name, value)

            for instance in instances.values():
                instance.save()

            validator = TravelCertificateValidator(
                document_number=document_number, 
                travel_certificate=travel_certificate
            )
            if validator.is_valid():
                try:
                    file_name = "travel_certificate.json"
                    configuration_file = os.path.join(
                        os.getcwd(),
                        "workresidentpermit",
                        "classes",
                        "production",
                        "configuration",
                        file_name
                    )
                    permit_data_processor = PermitDataProcessor(
                        configuration_file_name=configuration_file,
                        document_number=document_number
                    )
                    return Response(permit_data_processor.transform_data(), status=status.HTTP_201_CREATED)
                except Exception as e:
                    logging.error(f"Error processing permit data: {e}")
                    travel_certificate.delete()
                    return Response({"detail": "Internal server error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                travel_certificate.delete()
                return Response(validator.response.messages, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
