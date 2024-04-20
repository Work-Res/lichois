from ..api import WorkResidentPermitApplication
from app_personal_details.models import Person, Passport
from app_address.models import ApplicationAddress
from app_attachments.models import ApplicationAttachment

from ..models import Permit, Child, Spouse, WorkResidencePermit


class WorkResidentPermitData(object):

    def __init__(self, document_number):
        self.document_number = document_number
        self.work_resident_permit_application = WorkResidentPermitApplication()

    def data(self):
        return self.prepare()

    def prepare(self):
        self.work_resident_permit_application.personal_details = self.personal_details()
        self.work_resident_permit_application.passport = self.passport()
        self.work_resident_permit_application.address = self.address()
        self.work_resident_permit_application.permit = self.permit()
        # self.work_resident_permit_application.child = self.child()
        # self.work_resident_permit_application.spouse = self.spouse()
        self.work_resident_permit_application.form_details = self.form_details()
        # self.work_resident_permit_application.attachments = self.attachments()
        return self.work_resident_permit_application

    def personal_details(self):
        """
        TODO: review the join, may result in slow system.
        """
        try:
            person = Person.objects.get(
                application_version__application__application_document__document_number=self.document_number)
            return person
        except Person.DoesNotExist:
            pass

    def passport(self):
        try:
            passport = Passport.objects.get(
                application_version__application__application_document__document_number=self.document_number)
            return passport
        except Passport.DoesNotExist:
            pass

    def address(self):
        try:
            address = ApplicationAddress.objects.get(
                application_version__application__application_document__document_number=self.document_number)
            return address
        except ApplicationAddress.DoesNotExist:
            pass

    def permit(self):
        try:
            permit = Permit.objects.get(
                work_resident_permit__application_version__application__application_document__document_number=
                self.document_number)
            return permit
        except Permit.DoesNotExist:
            pass

    def child(self):
        child = Child.objects.filter(
            work_resident_permit__application_version__application__application_document__document_number=
            self.document_number)
        return child

    def spouse(self):
        spouse = Spouse.objects.filter(
            work_resident_permit__application_version__application__application_document__document_number=
            self.document_number)
        return spouse

    def form_details(self):
        try:
            form_details = WorkResidencePermit.objects.get(
                application_version__application__application_document__document_number=
                self.document_number)
            return form_details
        except WorkResidencePermit.DoesNotExist:
            pass

    def attachments(self):
        attachments = ApplicationAttachment.objects.filter(
            application_version__application__application_document__document_number=self.document_number)
        return attachments
