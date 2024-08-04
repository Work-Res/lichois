from identifier.identifier import Identifier

from citizenship.utils import CitizenshipProcessEnum


class CtizenshipDeprivationIdentifier(Identifier):

    template = '{identifier_type}{address_code}{dob}{sequence}'
    label = 'citizenship'
    identifier_type = 'CZDP'

    @staticmethod
    def process_name():
        return CitizenshipProcessEnum.CITIZENSHIP_DEPRIVATION.value
