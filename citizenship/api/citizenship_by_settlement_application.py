

class CitizenshipBySettlementApplication:
    """A wrapper class for work resident permit application details API model.
    """
    def __init__(self):
        self._personal_details = None
        self._address = None
        self._contacts = None
        self._personal_declaration = None
        self._dc_certificate = None
        self._citizenship_by_settlement = None


    @property
    def personal_details(self):
        return self._personal_details

    @personal_details.setter
    def personal_details(self, value):
        self._personal_details = value

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        self._address = value

    @property
    def contacts(self):
        return self._contacts

    @contacts.setter
    def contacts(self, value):
        self._contacts = value

    @property
    def personal_declaration(self):
        return self._personal_declaration

    @personal_declaration.setter
    def personal_declaration(self, value):
        self._personal_declaration = value

    @property
    def dc_certificate(self):
        return self._dc_certificate

    @dc_certificate.setter
    def dc_certificate(self, value):
        self._dc_certificate = value

    @property
    def citizenship_by_settlement(self):
        return self._citizenship_by_settlement

    @citizenship_by_settlement.setter
    def citizenship_by_settlement(self, value):
        self._citizenship_by_settlement = value

    # @property
    # def attachments(self):
    #     return self._attachments
    #
    # @attachments.setter
    # def attachments(self, value):
    #     self._attachments = value
    #
    #
    # @property
    # def report_details(self):
    #     return self._report_details
    #
    # @report_details.setter
    # def report_details(self, value):
    #     self._report_details = value
