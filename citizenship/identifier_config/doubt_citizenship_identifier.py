from identifier.identifier import Identifier

from citizenship.utils import CitizenshipProcessEnum


class DoubtCitizenshipCertificateIdentifier(Identifier):

    template = '{identifier_type}{address_code}{dob}{sequence}'
    label = 'citizenship'
    identifier_type = 'CZDBT'

    @staticmethod
    def process_name():
        return CitizenshipProcessEnum.DOUBT_CITIZENSHIP_CERTIFICATE.value
