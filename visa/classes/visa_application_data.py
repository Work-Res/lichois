from django.apps import apps
from ..api import VisaApplicationDetails
from app_personal_details.models import Person
from app_address.models import ApplicationAddress
from app_attachments.models import ApplicationAttachment
from app_contact.models import ApplicationContact
from ..models import VisaApplication


class VisaApplicationData(object):
	
	def __init__(self, document_number):
		self.document_number = document_number
		self.visa_application_details = VisaApplicationDetails()
	
	def data(self):
		return self.prepare()
	
	def prepare(self):
		self.visa_application_details.personal_details = self.personal_details()
		self.visa_application_details.contacts = self.contacts()
		self.visa_application_details.address = self.address()
		self.visa_application_details.attachments = self.attachments()
		self.visa_application_details.visa_application = self.visa_application()
		return self.visa_application_details

	def personal_details(self):
		"""
        TODO: review the join, may result in slow system.
        """
		return self.get_model_class(Person._meta.app_label.lower())

	def address(self):
		return self.get_model_class(ApplicationAddress._meta.app_label.lower())

	def contacts(self):
		return self.get_model_class(ApplicationContact._meta.app_label.lower())

	def visa_application(self):
		return self.get_model_class(VisaApplication._meta.app_label.lower())

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
