from identifier.identifier import Identifier

from citizenship.utils import CitizenshipProcessEnum


class SettlementIdentifier(Identifier):

    template = '{identifier_type}{address_code}{dob}{sequence}'
    label = 'citizenship'
    identifier_type = 'CZST'

    @staticmethod
    def process_name():
        return CitizenshipProcessEnum.SETTLEMENT.value
