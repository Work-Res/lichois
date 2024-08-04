from identifier.identifier import Identifier

from citizenship.utils import CitizenshipProcessEnum


class Under20CitizenshipIdentifier(Identifier):

    template = '{identifier_type}{address_code}{dob}{sequence}'
    label = 'citizenship'
    identifier_type = 'CZU20'

    @staticmethod
    def process_name():
        return CitizenshipProcessEnum.UNDER_20_CITIZENSHIP.value
