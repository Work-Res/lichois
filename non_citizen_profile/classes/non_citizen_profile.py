import re
from yaml import serialize
from ..api.serializers.profile import (
    AddressSerializer,
    BiometricsSerializer,
    ContactDetailsSerializer,
    EducationSerializer,
    NextOfKinSerializer,
    PassportSerializer,
    PersonalDetailsSerializer,
)
from ..models import (
    Address,
    Biometrics,
    ContactDetails,
    Education,
    NextOfKin,
    Passport,
    PersonalDetails,
)


class NonCitizenProfile:

    def __init__(self, identifier=None) -> None:
        self.non_citizen_identifier = identifier

    def get_address(self):
        try:
            obj = Address.objects.get(
                non_citizen_identifier=self.non_citizen_identifier
            )
            serializer = AddressSerializer(obj)
            return serializer.data
        except Address.DoesNotExist:
            return None

    def get_biometrics(self):
        try:
            obj = Biometrics.objects.get(
                non_citizen_identifier=self.non_citizen_identifier
            )
            serializer = BiometricsSerializer(obj)
            return serializer.data
        except Biometrics.DoesNotExist:
            return None

    def get_contact_details(self):
        try:
            obj = ContactDetails.objects.get(
                non_citizen_identifier=self.non_citizen_identifier
            )
            serializer = ContactDetailsSerializer(obj)
            return serializer.data
        except ContactDetails.DoesNotExist:
            return None

    def get_personal_details(self):
        try:
            obj = PersonalDetails.objects.get(
                non_citizen_identifier=self.non_citizen_identifier
            )
            serializer = PersonalDetailsSerializer(obj)
            return serializer.data
        except PersonalDetails.DoesNotExist:
            return None

    def get_education(self):
        try:
            obj = Education.objects.get(
                non_citizen_identifier=self.non_citizen_identifier
            )
            serializer = EducationSerializer(obj)
            return serializer.data
        except Education.DoesNotExist:
            return None

    def get_next_of_kin(self):
        try:
            obj = NextOfKin.objects.get(
                non_citizen_identifier=self.non_citizen_identifier
            )
            serializer = NextOfKinSerializer(obj)
            return serializer.data
        except NextOfKin.DoesNotExist:
            return None

    def get_passport(self):
        try:
            obj = Passport.objects.get(
                non_citizen_identifier=self.non_citizen_identifier
            )
            serializer = PassportSerializer(obj)
            return serializer.data
        except Passport.DoesNotExist:
            return None

    def get_combined_profile(self) -> dict:
        return {
            "address": self.get_address(),
            "biometrics": self.get_biometrics(),
            "contact_details": self.get_contact_details(),
            "personal_details": self.get_personal_details(),
            "education": self.get_education(),
            "next_of_kin": self.get_next_of_kin(),
            "passport": self.get_passport(),
        }

    def get_all_profiles(self):
        return PersonalDetailsSerializer(PersonalDetails.objects.all(), many=True).data
