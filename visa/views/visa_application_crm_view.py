import os
import logging
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers import VisaApplicationSerializer
from app_personal_details.models import Person, Passport
from app_address.models import ApplicationAddress
from app_contact.models import ApplicationContact
from ..models import DisposalMoney, VisaApplication,VisaReference
from ..validators import VisaValidator
from workresidentpermit.classes.production import PermitDataProcessor

class VisaApplicationCrmView(APIView):
    
    def post(self,request):
        serializer = VisaApplicationSerializer(data=request.data)
        if serializer.is_valid():
            visa_application = serializer.save()
            document_number = visa_application.document_number

            model_classes = {
                'app_personal_details_Person': Person,
                'app_address_ApplicationAddress': ApplicationAddress,
                'app_personal_details_Passport': Passport,
                'visa_Visa_Application': VisaApplication,
                'visa_Visa_Reference': VisaReference,
                'app_contact_Application_Contact': ApplicationContact,
                'visa_Disposal_Money': DisposalMoney
            }

            instances = {key: model() for key, model in model_classes.items()}
            instances['visa_Visa_Application'] = visa_application

            for key, value in request.data.items():
                parts = key.split('_')
                if len(parts) >= 3:
                    model_key = f"{parts[0]}_{parts[1]}"
                    field_name = '_'.join(parts[2:])
                    if model_key in instances and hasattr(instances[model_key], field_name):
                        setattr(instances[model_key], field_name, value)

            for instance in instances.values():
                instance.save()

            validator = VisaValidator(
                document_number=document_number, 
                visa_application=visa_application
            )
            if validator.is_valid():
                try:
                    file_name = "visa_application.json"
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
                    visa_application.delete()
                    return Response({"detail": "Internal server error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                visa_application.delete()
                return Response(validator.response.messages, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
