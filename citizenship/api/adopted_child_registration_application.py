

class AdoptedChildRegistrationApplication:
    """A wrapper class for work resident permit application details API model.
    """
    def __init__(self):
        self._guardian_personal_details = None
        self._guardian_contact_details = None
        self._guardian_oath = None
        self._child_personal_details = None
        self._child_address_details = None
        self._parent_personal_details = None
        self._parent_address_details = None
        self._sponsors_personal_details = None
        self._sponsors_address_details = None
        self._witness_personal_details = None
        self._witness_address_details = None
        self._additional_sponsors_personal_details = None
        self._additional_sponsors_address_details = None
        self._additional_witness_personal_details = None
        self._additional_witness_address_details = None


    @property
    def guardian_personal_details(self):
        return self._guardian_personal_details

    @guardian_personal_details.setter
    def guardian_personal_details(self, value):
        self._guardian_personal_details = value

    @property
    def guardian_contact_details(self):
        return self._guardian_contact_details

    @guardian_contact_details.setter
    def guardian_contact_details(self, value):
        self._guardian_contact_details = value

    @property
    def guardian_oath(self):
        return self._guardian_oath

    @guardian_oath.setter
    def guardian_oath(self, value):
        self.guardian_oath = value

    @property
    def child_personal_details(self):
        return self._child_personal_details

    @child_personal_details.setter
    def child_personal_details(self, value):
        self._child_personal_details = value

    @property
    def child_address_details(self):
        return self._child_address_details

    @child_address_details.setter
    def child_address_details(self, value):
        self._child_address_details = value

    @property
    def parent_personal_details(self):
        return self._parent_personal_details

    @parent_personal_details.setter
    def parent_personal_details(self, value):
        self._parent_personal_details = value

    @property
    def parent_address_details(self):
        return self._parent_address_details

    @parent_address_details.setter
    def parent_address_details(self, value):
        self._parent_address_details = value

    @property
    def sponsors_personal_details(self):
        return self._sponsors_personal_details

    @sponsors_personal_details.setter
    def sponsors_personal_details(self, value):
        self._sponsors_personal_details = value

    @property
    def sponsors_address_details(self):
        return self._sponsors_address_details

    @sponsors_address_details.setter
    def sponsors_address_details(self, value):
        self._sponsors_address_details = value

    @property
    def witness_personal_details(self):
        return self._witness_personal_details

    @witness_personal_details.setter
    def witness_personal_details(self, value):
        self._witness_personal_details = value

    @property
    def witness_address_details(self):
        return self._witness_address_details

    @witness_address_details.setter
    def witness_address_details(self, value):
        self._witness_address_details = value

    @property
    def additional_sponsors_personal_details(self):
        return self._additional_sponsors_personal_details

    @additional_sponsors_personal_details.setter
    def additional_sponsors_personal_details(self, value):
        self._additional_sponsors_personal_details = value

    @property
    def additional_sponsors_address_details(self):
        return self._additional_sponsors_address_details

    @additional_sponsors_address_details.setter
    def additional_sponsors_address_details(self, value):
        self._additional_sponsors_address_details = value

    @property
    def additional_witness_personal_details(self):
        return self._additional_witness_personal_details

    @additional_witness_personal_details.setter
    def additional_witness_personal_details(self, value):
        self._additional_witness_personal_details = value

    @property
    def additional_witness_address_details(self):
        return self._additional_witness_address_details

    @additional_witness_address_details.setter
    def additional_witness_address_details(self, value):
        self._additional_witness_address_details = value


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
