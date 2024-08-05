from identifier.identifier import Identifier

from citizenship.utils import CitizenshipProcessEnum


class ForeignSpouseNaturalizationIdentifier(Identifier):

    template = '{identifier_type}{address_code}{dob}{sequence}'
    label = 'citizenship'
    identifier_type = 'CZFSN'

    @staticmethod
    def process_name():
        return CitizenshipProcessEnum.FOREIGN_SPOUSE_NATURALIZATION.value
