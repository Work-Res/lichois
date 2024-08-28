from ..models import (
    Address,
    Biometrics,
    ContactDetails,
    PersonalDetails,
    Education,
    NextOfKin,
    Passport,
)


class NonCitizenProfile:

    def ___init__(self, non_citizen_identifier) -> None:
        self.non_citizen_identifier = non_citizen_identifier

    def get_address(self) -> Address | None:
        try:
            return Address.objects.get(
                non_citizen_identifier=self.non_citizen_identifier
            )
        except Address.DoesNotExist:
            return None

    def get_biometrics(self) -> Biometrics | None:
        try:
            return Biometrics.objects.get(
                non_citizen_identifier=self.non_citizen_identifier
            )
        except Biometrics.DoesNotExist:
            return None

    def get_contact_details(self) -> ContactDetails | None:
        try:
            return ContactDetails.objects.get(
                non_citizen_identifier=self.non_citizen_identifier
            )
        except ContactDetails.DoesNotExist:
            return None

    def get_personal_details(self) -> PersonalDetails | None:
        try:
            return PersonalDetails.objects.get(
                non_citizen_identifier=self.non_citizen_identifier
            )
        except PersonalDetails.DoesNotExist:
            return None

    def get_education(self) -> Education | None:
        try:
            return Education.objects.get(
                non_citizen_identifier=self.non_citizen_identifier
            )
        except Education.DoesNotExist:
            return None

    def get_next_of_kin(self) -> NextOfKin | None:
        try:
            return NextOfKin.objects.get(
                non_citizen_identifier=self.non_citizen_identifier
            )
        except NextOfKin.DoesNotExist:
            return None

    def get_passport(self) -> Passport | None:
        try:
            return Passport.objects.get(
                non_citizen_identifier=self.non_citizen_identifier
            )
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
        }
