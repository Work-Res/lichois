from venv import logger
from app_personal_details.api.serializers import PermitSerializer
from app_personal_details.models.permit import Permit
from ..api.serializers.profile import (
    AddressSerializer,
    BiometricsSerializer,
    ContactDetailsSerializer,
    EducationSerializer,
    NextOfKinSerializer,
    PassportSerializer,
    PersonalDetailsSerializer,
)
from app_personal_details.models import (
    Passport,
    Person,
    Education,
    NextOfKin,
)
from ..models import Biometrics
from app_address.models import ApplicationAddress
from app_contact.models import ApplicationContact


import logging


class NonCitizenProfile:

    def __init__(
        self, identifier=None, first_name=None, last_name=None, permit_number=None
    ) -> None:
        self.non_citizen_identifier = identifier
        self.first_name = first_name
        self.last_name = last_name
        self.permit_number = permit_number
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

    def get_address(self):
        return self.get_data(ApplicationAddress, AddressSerializer)

    def get_biometrics(self):
        return self.get_data(Biometrics, BiometricsSerializer)

    def get_contact_details(self):
        return self.get_data(ApplicationContact, ContactDetailsSerializer)

    def get_personal_details(self):
        return self.get_data(Person, PersonalDetailsSerializer)

    def get_education(self):
        return self.get_data(Education, EducationSerializer)

    def get_next_of_kin(self):
        return self.get_data(NextOfKin, NextOfKinSerializer)

    def get_passport(self):
        return self.get_data(Passport, PassportSerializer)

    def get_permit_number(self):
        return self.get_data(Permit, PermitSerializer)

    def get_combined_profile(self) -> dict:
        return {
            "address": self.get_address(),
            "biometrics": self.get_biometrics(),
            "contact_details": self.get_contact_details(),
            "personal_details": self.get_personal_details(),
            "education": self.get_education(),
            "next_of_kin": self.get_next_of_kin(),
            "passport": self.get_passport(),
            "permit_number": self.get_permit_number(),
        }

    def get_all_profiles(self):
        return PersonalDetailsSerializer(
            Person.objects.filter(**self.get_filters()), many=True
        ).data

    def get_filters(self):
        filters = {}
        if self.non_citizen_identifier:
            filters["non_citizen_identifier"] = self.non_citizen_identifier
        if self.first_name:
            filters["first_name__icontains"] = self.first_name
        if self.last_name:
            filters["last_name__icontains"] = self.last_name
        return filters

    def get_data(self, model, serializer):
        try:
            obj = model.objects.get(non_citizen_identifier=self.non_citizen_identifier)
            serialized_data = serializer(obj)
            return serialized_data.data
        except model.DoesNotExist:
            return None
        except model.MultipleObjectsReturned:
            # return one object
            obj = model.objects.filter(
                non_citizen_identifier=self.non_citizen_identifier
            ).first()
            serialized_data = serializer(obj)
            return serialized_data.data
        except Exception as e:
            self.logger.error(f"Error getting {model.__name__} data: {e}")
            return str(e)
