from django.apps import apps
from ..api import CertNaturalisationForeignSpouseApplication
from app_address.models import ApplicationAddress
from app_contact.models import ApplicationContact
from app_personal_details.models import Person
from ..models import CertNaturalisationByForeignSpouse, SpouseInfo, ParentDetails


class CertNaturalisationForeignSpouseData(object):

    def __init__(self, document_number):
        self.document_number = document_number
        self.cert_intention_foreign_spouse_application = CertNaturalisationForeignSpouseApplication()

    def data(self):
        return self.prepare()

    def prepare(self):
        self.cert_intention_foreign_spouse_application.personal_details = self.personal_details
        self.cert_intention_foreign_spouse_application.contacts = self.contacts()
        self.cert_intention_foreign_spouse_application.address = self.address()
        self.cert_intention_foreign_spouse_application.spouse_info = self.spouse_info()
        self.cert_intention_foreign_spouse_application.parent_details = self.parent_details()
        self.cert_intention_foreign_spouse_application.naturalisation_fs_application = self.naturalisation_fs_application()
        return self.cert_intention_foreign_spouse_application

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

	def parent_details(self):
		"""
		"""  # TODO: define the relationship for onetomany, foreignkey?
		# parent_details = ParentDetails.objects.filter(
		# 	work_resident_permit__document_number=self.document_number)
		return  # parent_details

    def naturalisation_fs_application(self):
        return self.get_model_class(CertNaturalisationByForeignSpouse._meta.app_label.lower())

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
