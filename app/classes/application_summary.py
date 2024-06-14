import re

from django.apps import apps

from app_attachments.api.serializers import ApplicationAttachmentSerializer


class ApplicationSummary(object):
	
	def __init__(self, document_number, app_labels):
		self.document_number = document_number
		self.app_labels = app_labels
	
	def data(self):
		summary = {}
		for app_label in self.get_app_label():
			model_name = apps.get_model(app_label).__name__
			snake_case_model_name = self.to_snake_case(model_name)
			form_details = self.get_model(app_label)
			if form_details is not None:
				summary[snake_case_model_name] = self.serialize_model(form_details)
			summary['attachments'] = self.get_attachments()
		return summary
	
	def get_model(self, app_label):
		""" Get the model instance based on app label, model name, and document number. """
		model_cls = apps.get_model(app_label)
		try:
			return model_cls.objects.get(document_number=self.document_number)
		except model_cls.DoesNotExist:
			return None
		
	def get_attachments(self):
		""" Get the attachments based on the document number. """
		attachment_models = apps.get_model('app_attachments.ApplicationAttachment').objects.filter(
			document_number=self.document_number)
		attachments = ApplicationAttachmentSerializer(attachment_models, many=True).data
		return attachments
	
	def serialize_model(self, model_instance):
		""" Serialize model instance to a dictionary. """
		serialized_data = {}
		fields = model_instance._meta.get_fields()
		for field in fields:
			field_name = field.name
			if field_name == 'application_version':
				# Handle the serialization of ApplicationVersion separately
				serialized_data[field_name] = self.serialize_application_version(getattr(model_instance, field_name))
			else:
				# Serialize other fields as usual
				serialized_data[field_name] = getattr(model_instance, field_name)
		return serialized_data
	
	def to_snake_case(self, camel_str):
		""" Convert a CamelCase string to snake_case."""
		return re.sub('([a-z0-9])([A-Z])', r'\1_\2', camel_str).lower()
	
	def serialize_application_version(self, application_version):
		""" Serialize ApplicationVersion instance to a dictionary. """
		if application_version is not None:
			# You can customize this serialization process according to your requirements
			return {
				'id': application_version.id,
				'version_number': application_version.version_number,
				# Include other fields as needed
			}
		else:
			return None
		
	def get_app_label(self) -> list:
		""" Get the list of app labels to be used in the summary. """
		generic_label = [
			'app_personal_details.Person',
			'app_address.ApplicationAddress',
			'app_contact.ApplicationContact',
			'app_personal_details.Passport',
		]
		generic_label.extend(self.app_labels)
		return generic_label
