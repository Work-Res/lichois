from identifier.identifier import Identifier

from citizenship.utils import CitizenshipProcessEnum


class NaturalizationIdentifier(Identifier):

    template = '{identifier_type}{address_code}{dob}{sequence}'
    label = 'citizenship'
    identifier_type = 'CZN'

    @staticmethod
    def process_name():
        return CitizenshipProcessEnum.NATURALIZATION.value
