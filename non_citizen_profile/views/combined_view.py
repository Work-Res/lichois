from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Address, Biometrics, ContactDetails, Passport, PersonalDetails, Education, NextOfKin
from api.serializers import CombinedSerializer

class CombinedView(APIView):
    def get(self, request, *args, **kwargs):
        # Fetch data from all models
        address = Address.objects.all().first() 
        biometrics = Biometrics.objects.all().first()
        contact_details = ContactDetails.objects.all().first()
        passport = Passport.objects.all().first()
        personal_details = PersonalDetails.objects.all().first()
        education = Education.objects.all().first()
        next_of_kin = NextOfKin.objects.all().first()
        
        # Check if all data is available
        if not all([address, biometrics, contact_details, passport, personal_details, education, next_of_kin]):
            return Response({"detail": "One or more resources not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CombinedSerializer({
            "address": address,
            "biometrics": biometrics,
            "contact_details": contact_details,
            "passport": passport,
            "personal_details": personal_details,
            "education": education,
            "next_of_kin": next_of_kin
        })

        return Response(serializer.data, status=status.HTTP_200_OK)