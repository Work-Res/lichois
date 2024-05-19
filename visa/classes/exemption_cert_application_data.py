from django.apps import apps
from ..api import ExemptionCertApplicationDetails
from app_personal_details.models import Person, Passport
from app_address.models import ApplicationAddress
from app_attachments.models import ApplicationAttachment
from app_contact.models import ApplicationContact
from ..models import ExemptionCertificateApplication


class ExemptionCertApplicationData(object):
	
	def __init__(self, document_number):
		self.document_number = document_number
		self.exemption_cert_application_details = ExemptionCertApplicationDetails()
	
	def data(self):
		return self.prepare()
	
	def prepare(self):
		self.exemption_cert_application_details.personal_details = self.personal_details()
		self.exemption_cert_application_details.passport = self.passport()
		self.exemption_cert_application_details.contacts = self.contacts()
		self.exemption_cert_application_details.address = self.address()
		self.exemption_cert_application_details.attachments = self.attachments()
		self.exemption_cert_application_details.exemption_cert_application = self.exemption_cert_application()
		return self.exemption_cert_application_details

	def personal_details(self):
		"""
        TODO: review the join, may result in slow system.
        """
		return self.get_model_class(Person._meta.app_label.lower())

	def passport(self):
		return self.get_model_class(Passport._meta.app_label.lower())

	def contacts(self):
		return self.get_model_class(ApplicationContact._meta.app_label.lower())

	def address(self):
		return self.get_model_class(ApplicationAddress._meta.app_label.lower())

	def exemption_cert_application(self):
		return self.get_model_class(ExemptionCertificateApplication._meta.app_label.lower())

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
