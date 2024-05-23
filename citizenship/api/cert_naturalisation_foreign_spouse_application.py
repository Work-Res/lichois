

class CertNaturalisationForeignSpouseApplication:
    """A wrapper class for work resident permit application details API model.
    """
    def __init__(self):
        self._personal_details = None
        self._address = None
        self._contacts = None
        self._spouse_info = None
        self._parental_details = None
        self._naturalisation_fs_application = None

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
    def parental_details(self):
        return self._parental_details

    @parental_details.setter
    def parental_details(self, value):
        self._parental_details = value


    @property
    def naturalisation_fs_application(self):
        return self._naturalisation_fs_application

    @naturalisation_fs_application.setter
    def naturalisation_fs_application(self, value):
        self._naturalisation_fs_application = value

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
