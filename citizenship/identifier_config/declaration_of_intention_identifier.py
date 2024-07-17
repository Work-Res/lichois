
from identifier.identifier import Identifier

from citizenship.utils import CitizenshipProcessEnum


class DeclarationOfIntentionIdentifier(Identifier):
    template = '{identifier_type}{address_code}{dob}{sequence}'
    label = 'citizenship'
    identifier_type = 'CZDIF'

    @staticmethod
    def process_name():
        return CitizenshipProcessEnum.INTENTION_FOREIGN_SPOUSE.value
