

class VisaApplicationDetails:
    """A wrapper class for work resident permit application details API model.
    """
    def __init__(self):
        self._personal_details = None
        self._contacts = None
        self._address = None
        self._attachments = None
        self._visa_application = None


    @property
    def personal_details(self):
        return self._personal_details

    @personal_details.setter
    def personal_details(self, value):
        self._personal_details = value

    @property
    def contacts(self):
        return self._contacts

    @contacts.setter
    def contacts(self, value):
        self._contacts = value

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        self._address = value

    @property
    def attachments(self):
        return self._attachments

    @attachments.setter
    def attachments(self, value):
        self._attachments = value

    @property
    def visa_application(self):
        return self._visa_application

    @visa_application.setter
    def visa_application(self, value):
        self._visa_application = value

    # @property
    # def report_details(self):
    #     return self._report_details
    #
    # @report_details.setter
    # def report_details(self, value):
    #     self._report_details = value
