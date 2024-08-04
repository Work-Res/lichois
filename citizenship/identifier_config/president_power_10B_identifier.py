from identifier.identifier import Identifier

from citizenship.utils import CitizenshipProcessEnum


class PresidentPower10BIdentifier(Identifier):

    template = '{identifier_type}{address_code}{dob}{sequence}'
    label = 'citizenship'
    identifier_type = 'CZPPB'

    @staticmethod
    def process_name():
        return CitizenshipProcessEnum.PRESIDENT_POWER_10B.value
