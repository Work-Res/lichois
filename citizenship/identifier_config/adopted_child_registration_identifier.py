from identifier.identifier import Identifier

from citizenship.utils import CitizenshipProcessEnum


class AdoptedChildRegistrationIdentifier(Identifier):

    template = '{identifier_type}{address_code}{dob}{sequence}'
    label = 'citizenship'
    identifier_type = 'CZACR'

    @staticmethod
    def process_name():
        return CitizenshipProcessEnum.ADOPTED_CHILD_REGISTRATION.value
