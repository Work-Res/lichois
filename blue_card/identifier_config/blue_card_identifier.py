from identifier.identifier import Identifier


class BlueCardPermitIdentifier(Identifier):
    template = "{identifier_type}{address_code}{dob}{sequence}"
    label = "bluecardpermit"  # e.g. work_permit_identifier, visa_identifier, etc
    identifier_type = "BC"

    @staticmethod
    def process_name():
        return "BLUE_CARD_PERMIT"


class BlueCardReplacementIdentifier(Identifier):
    template = "{identifier_type}{address_code}{dob}{sequence}"
    label = "bluecardpermit"  # e.g. work_permit_identifier, visa_identifier, etc
    identifier_type = "BCR"

    @staticmethod
    def process_name():
        return "BLUE_CARD_REPLACEMENT"

class BlueCardReturnsIdentifier(Identifier):
    template = "{identifier_type}{address_code}{dob}{sequence}"
    label = "bluecardpermit"  # e.g. work_permit_identifier, visa_identifier, etc
    identifier_type = "BCX"

    @staticmethod
    def process_name():
        return "BLUE_CARD_RETURNS"