

class RenunciationOfForeignCitizenshipApplication:
    """A wrapper class for naturalisation application details API model.
    """
    def __init__(self):
        self._personal_details = None
        self._address = None
        self._contacts = None
        self._spouse_info = None
        self._oath_of_allegiance = None
        self._renunciation_foreign_citizenship_application = None

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
    def spouse_info(self):
        return self._spouse_info

    @spouse_info.setter
    def spouse_info(self, value):
        self._spouse_info = value

    @property
    def oath_of_allegiance(self):
        return self._oath_of_allegiance

    @oath_of_allegiance.setter
    def oath_of_allegiance(self, value):
        self._oath_of_allegiance = value

    @property
    def renunciation_foreign_citizenship_application(self):
        return self._renunciation_foreign_citizenship_application

    @renunciation_foreign_citizenship_application.setter
    def renunciation_foreign_citizenship_application(self, value):
        self._renunciation_foreign_citizenship_application = value

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
