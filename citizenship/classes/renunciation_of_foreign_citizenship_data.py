from django.apps import apps
from ..api import RenunciationOfForeignCitizenshipApplication
from app_personal_details.models import Person
from app_address.models import ApplicationAddress
from app_attachments.models import ApplicationAttachment
from app_contact.models import ApplicationContact
from ..models import RenunciationOfForeignCitizenship, SpouseInfo, OathOfAllegiance


class RenunciationOfForeignCitizenshipData(object):

    def __init__(self, document_number):
        self.document_number = document_number
        self.foreign_citizenship_renunciation = RenunciationOfForeignCitizenshipApplication()

    def data(self):
        return self.prepare()

    def prepare(self):
        self.foreign_citizenship_renunciation.personal_details = self.personal_details
        self.foreign_citizenship_renunciation.contacts = self.contacts()
        self.foreign_citizenship_renunciation.address = self.address()
        self.foreign_citizenship_renunciation.spouse_info = self.spouse_info()
        self.foreign_citizenship_renunciation.oath_of_allegiance = self.oath_of_allegiance()
        self.foreign_citizenship_renunciation.renunciation_foreign_citizenship_application = self._renunciation_foreign_citizenship_application()
        return self.foreign_citizenship_renunciation

    def personal_details(self):
        """
        TODO: review the join, may result in slow system.
        """
        return self.get_model_class(Person._meta.app_label.lower())

    def address(self):
        return self.get_model_class(ApplicationAddress._meta.app_label.lower())

    def contacts(self):
        return self.get_model_class(ApplicationContact._meta.app_label.lower())

    def spouse_info(self):
        return self.get_model_class(SpouseInfo._meta.app_label.lower())

    def oath_of_allegiance(self):
        return self.get_model_class(OathOfAllegiance._meta.app_label.lower())

    def renunciation_foreign_citizenship_application(self):
        return self.get_model_class(RenunciationOfForeignCitizenship._meta.app_label.lower())

    # def attachments(self):
    # 	attachments = ApplicationAttachment.objects.filter(
    # 		application_version__application__application_document__document_number=self.document_number)
    # 	return attachments

    def get_model_class(self, model_string):
        try:
            app_label, model_name = model_string.split('.')
            model_cls = apps.get_model(app_label, model_name)
        except ValueError:
            raise ValueError("Model string must be in the format 'app_label.ModelName'")
        except LookupError:
            raise LookupError(f"Model '{model_string}' not found")
        else:
            try:
                form_details = model_cls.objects.get(document_number=self.document_number)
                return form_details
            except model_cls.DoesNotExist:
                pass
