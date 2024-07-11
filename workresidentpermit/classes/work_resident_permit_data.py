import logging
from typing import Optional

from app.models import ApplicationVerification
from app_address.models import ApplicationAddress
from app_attachments.models import ApplicationAttachment
from app_contact.models import ApplicationContact
from app_personal_details.models import Passport, Permit, Person
from board.models import BoardDecision

from ..api import WorkResidentPermitApplication
from ..models import Child, ResidencePermit, SecurityClearance, Spouse, WorkPermit

logger = logging.getLogger(__name__)


class WorkResidentPermitData(object):

    def __init__(self, document_number):

        self.document_number = document_number
        self.work_resident_permit_application = WorkResidentPermitApplication()

    def data(self):
        return self.prepare()

    def prepare(self):
        self.work_resident_permit_application.personal_details = self.personal_details()
        self.work_resident_permit_application.passport = self.passport()
        self.work_resident_permit_application.contacts = self.contacts()
        self.work_resident_permit_application.address = self.address()
        self.work_resident_permit_application.permit = self.permit()
        self.work_resident_permit_application.child = self.child()
        self.work_resident_permit_application.spouse = self.spouse()
        self.work_resident_permit_application.resident_permit = self.resident_permit()
        self.work_resident_permit_application.work_permit = self.work_permit()
        self.work_resident_permit_application.attachments = self.attachments()
        self.work_resident_permit_application.application = self.application()
        self.work_resident_permit_application.security_clearance = (
            self.security_clearance()
        )
        self.work_resident_permit_application.board_decision = self.board_decision()
        self.work_resident_permit_application.application_verification = (
            self.application_verification()
        )
        return self.work_resident_permit_application

    def personal_details(self):
        """
        TODO: review the join, may result in slow system.
        """
        try:
            person = Person.objects.get(document_number=self.document_number)
            return person
        except Person.DoesNotExist:
            pass

    def passport(self):
        try:
            passport = Passport.objects.get(document_number=self.document_number)
            return passport
        except Passport.DoesNotExist:
            pass

    def address(self):
        try:
            address = ApplicationAddress.objects.get(
                document_number=self.document_number
            )
            return address
        except ApplicationAddress.DoesNotExist:
            pass

    def permit(self):
        try:
            permit = Permit.objects.get(document_number=self.document_number)
            return permit
        except Permit.DoesNotExist:
            pass

    def child(self):
        child = Child.objects.filter(
            work_resident_permit__document_number=self.document_number
        )
        return child

    def spouse(self):
        spouse = Spouse.objects.filter(
            work_resident_permit__document_number=self.document_number
        )
        return spouse

    def contacts(self):
        try:
            contacts = ApplicationContact.objects.get(
                document_number=self.document_number
            )
            return contacts
        except ApplicationContact.DoesNotExist:
            pass

    def resident_permit(self):
        try:
            form_details = ResidencePermit.objects.get(
                document_number=self.document_number
            )
            return form_details
        except ResidencePermit.DoesNotExist:
            pass

    def work_permit(self):
        try:
            form_details = WorkPermit.objects.get(document_number=self.document_number)
            return form_details
        except WorkPermit.DoesNotExist:
            pass

    def attachments(self):
        attachments = ApplicationAttachment.objects.filter(
            application_version__application__application_document__document_number=self.document_number
        )
        return attachments

    def application(self):
        application = None
        if self.resident_permit():
            application = self.resident_permit().application_version.application
        elif self.work_permit():
            application = self.work_permit().application_version.application
        return application

    def application_verification(self) -> Optional[ApplicationVerification]:
        """
        Attempts to retrieve an ApplicationVerification object by the document number.

        Returns:
            ApplicationVerification: The verification object if found.
            None: If no verification object is found.
        """
        try:
            return ApplicationVerification.objects.get(
                document_number=self.document_number
            )
        except ApplicationVerification.DoesNotExist:
            return None

    def security_clearance(self) -> Optional[SecurityClearance]:
        """
        Attempts to retrieve a SecurityClearance object by the document number.

        Returns:
            SecurityClearance: The security clearance object if found.
            None: If no security clearance object is found.
        """
        try:
            return SecurityClearance.objects.get(document_number=self.document_number)
        except SecurityClearance.DoesNotExist:
            logger.info(
                f"SecurityClearance with document number {self.document_number} does not exist."
            )
            return None

    def board_decision(self) -> Optional[BoardDecision]:
        """
        Attempts to retrieve a BoardDecision object associated with the given document number.

        Returns:
            BoardDecision: The board decision object if found.
            None: If no board decision object is found.
        """
        try:
            return BoardDecision.objects.get(
                assessed_application__application_document__document_number=self.document_number
            )
        except BoardDecision.DoesNotExist:
            logger.info(
                f"BoardDecision with document number {self.document_number} does not exist."
            )
            return None
