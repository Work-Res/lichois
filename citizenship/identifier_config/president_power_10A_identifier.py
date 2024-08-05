from identifier.identifier import Identifier

from citizenship.utils import CitizenshipProcessEnum


class PresidentPower10AIdentifier(Identifier):

    template = '{identifier_type}{address_code}{dob}{sequence}'
    label = 'citizenship'
    identifier_type = 'CZPPA'

    @staticmethod
    def process_name():
        return CitizenshipProcessEnum.PRESIDENT_POWER_10A.value
