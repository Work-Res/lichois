import re

from django.apps import apps


class ApplicationSummary(object):
	
	def __init__(self, document_number, app_labels):
		self.document_number = document_number
		self.app_labels = app_labels

	def data(self):
		summary = {
			self.to_snake_case(apps.get_model(app_label).__name__): self.get_model(app_label) for app_label in self.app_labels
		}
		return summary
	
	def get_model(self, app_label):
		""" Get the model instance based on app label, model name, and document number. """
		model_cls = apps.get_model(app_label)
		try:
			form_details = model_cls.objects.get(document_number=self.document_number)
			return form_details
		except model_cls.DoesNotExist:
			pass
		return None
	
	def to_snake_case(self, camel_str):
		""" Convert a CamelCase string to snake_case."""
		return re.sub('([a-z0-9])([A-Z])', r'\1_\2', camel_str).lower()

