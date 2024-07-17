from identifier.identifier import Identifier


class RenunciationIdentifier(Identifier):
    template = '{identifier_type}{address_code}{dob}{sequence}'
    label = 'citizenship'
    identifier_type = 'CZR'

    @staticmethod
    def process_name():
        return 'citizenship_renunciation'
