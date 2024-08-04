from identifier.identifier import Identifier

from citizenship.utils import CitizenshipProcessEnum


class CitizenshipResumptionIdentifier(Identifier):

    template = '{identifier_type}{address_code}{dob}{sequence}'
    label = 'citizenship'
    identifier_type = 'CZRS'

    @staticmethod
    def process_name():
        return CitizenshipProcessEnum.CITIZENSHIP_RESUMPTION.value
