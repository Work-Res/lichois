from identifier.identifier import Identifier

from citizenship.utils import CitizenshipProcessEnum


class MaturityPeriodWaiverIdentifier(Identifier):

    template = '{identifier_type}{address_code}{dob}{sequence}'
    label = 'citizenship'
    identifier_type = 'CZMPW'

    @staticmethod
    def process_name():
        return CitizenshipProcessEnum.MATURITY_PERIOD_WAIVER.value