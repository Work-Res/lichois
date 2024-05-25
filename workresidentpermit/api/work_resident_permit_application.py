

class WorkResidentPermitApplication:
    """A wrapper class for work resident permit application details API model.
    """
    def __init__(self):
        self._personal_details = None
        self._address = None
        self._contacts = None
        self._passport = None
        self._permit = None
        self._child = None
        self._spouse = None
        self._resident_permit = None
        self._application = None
        self._attachments = None
        self._report_details = None
        self._work_permit = None
        self._security_clearance = None
        self._board_decision = None
        self._application_verification = None

    @property
    def security_clearance(self):
        return self._security_clearance

    @security_clearance.setter
    def security_clearance(self, value):
        self._security_clearance = value

    @property
    def board_decision(self):
        return self._board_decision

    @board_decision.setter
    def board_decision(self, value):
        self._board_decision = value

    @property
    def application_verification(self):
        return self._application_verification

    @application_verification.setter
    def application_verification(self, value):
        self._application_verification = value

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
    def passport(self):
        return self._passport

    @passport.setter
    def passport(self, value):
        self._passport = value

    @property
    def permit(self):
        return self._permit

    @permit.setter
    def permit(self, value):
        self._permit = value

    @property
    def child(self):
        return self._child

    @child.setter
    def child(self, value):
        self._child = value

    @property
    def spouse(self):
        return self._spouse

    @spouse.setter
    def spouse(self, value):
        self._spouse = value

    @property
    def resident_permit(self):
        return self._resident_permit

    @resident_permit.setter
    def resident_permit(self, value):
        self._resident_permit = value
    
    @property
    def work_permit(self):
        return self._work_permit
    
    @work_permit.setter
    def work_permit(self, value):
        self._work_permit = value

    @property
    def application(self):
        return self._application

    @application.setter
    def application(self, value):
        self._application = value

    @property
    def attachments(self):
        return self._attachments

    @attachments.setter
    def attachments(self, value):
        self._attachments = value

    @property
    def contacts(self):
        return self._contacts

    @contacts.setter
    def contacts(self, value):
        self._contacts = value

    @property
    def report_details(self):
        return self._report_details

    @report_details.setter
    def report_details(self, value):
        self._report_details = value
