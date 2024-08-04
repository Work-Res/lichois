from identifier.identifier import Identifier

from citizenship.utils import CitizenshipProcessEnum


class DualRenunciationIdentifier(Identifier):

    template = '{identifier_type}{address_code}{dob}{sequence}'
    label = 'citizenship'
    identifier_type = 'CZDR'

    @staticmethod
    def process_name():
        return CitizenshipProcessEnum.DUAL_RENUNCIATION.value
