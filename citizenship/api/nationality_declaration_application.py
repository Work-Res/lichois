

class NationalityDeclarationApplication:
    """A wrapper class for nationality declaration application details API model.
    """

    def __init__(self):
        self._personal_details = None
        self._address = None
        self._contacts = None
        self._place_of_residence = None
        self._parental_details = None
        self._nationality_declaration = None

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
    def parental_details(self):
        return self._parental_details

    @parental_details.setter
    def parental_details(self, value):
        self._parental_details = value

    @property
    def place_of_residence(self):
        return self._place_of_residence

    @place_of_residence.setter
    def place_of_residence(self, value):
        self._place_of_residence = value

    @property
    def nationality_declaration(self):
        return self._nationality_declaration

    @nationality_declaration.setter
    def nationality_declaration(self, value):
        self._nationality_declaration = value

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
