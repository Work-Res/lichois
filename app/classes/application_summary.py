import re
from django.apps import apps
from django.db.models import ForeignKey, ManyToManyField, QuerySet
from django.forms import model_to_dict

from app_attachments.api.serializers import ApplicationAttachmentSerializer

class ApplicationSummary:
    def __init__(self, document_number, app_labels):
        self.document_number = document_number
        self.app_labels = app_labels

    def data(self):
        summary = {}
        for app_label in self.get_app_labels():
            model_instance = self.get_model_instance(app_label)
            if model_instance:
                model_name = apps.get_model(app_label).__name__
                snake_case_model_name = self.to_snake_case(model_name)
                summary[snake_case_model_name] = self.serialize_model_instance(model_instance)
        return summary

    def get_model_instance(self, app_label):
        """Get the model instance based on app label and document number."""
        model_cls = apps.get_model(app_label)
        return model_cls.objects.filter(document_number=self.document_number).first()
    
    def serialize_model_instance(self, model_instance):
        """Serialize model instance to a dictionary."""
        serialized_data = {}
        for field in model_instance._meta.get_fields():
            field_name = field.name
            try:
                if isinstance(field, ForeignKey):
                    # Handle ForeignKey relationships
                    related_instance = getattr(model_instance, field_name)
                    if related_instance:
                        serialized_data[field_name] = self.serialize_related_instance(related_instance)
                    else:
                        serialized_data[field_name] = None
                elif isinstance(field, ManyToManyField):
                    # Skip ManyToManyField since it's not the case
                    continue
                else:
                    # Handle other fields normally
                    serialized_data[field_name] = getattr(model_instance, field_name)
            except AttributeError as e:
                # Handle the case where an attribute doesn't exist on the model instance
                print(f"Error accessing field '{field_name}' on {model_instance}: {e}")
                serialized_data[field_name] = None
        
        return serialized_data
    
    def serialize_related_instance(self, related_instance):
        """Serialize related instance (ForeignKey or queryset) to a dictionary."""
        if isinstance(related_instance, QuerySet):
            # Handle queryset of related instances
            serialized_data = [model_to_dict(instance, fields=[field.name for field in instance._meta.fields]) for instance in related_instance]
        else:
            # Handle ForeignKey relationships
            serialized_data = model_to_dict(related_instance, fields=[field.name for field in related_instance._meta.fields])
        return serialized_data

    @staticmethod
    def to_snake_case(camel_str):
        """Convert a CamelCase string to snake_case."""
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', camel_str).lower()

    def get_app_labels(self):
        """Get the list of app labels to be used in the summary."""
        generic_labels = [
            'app_personal_details.Person',
            'app_address.ApplicationAddress',
            'app_contact.ApplicationContact',
            'app_personal_details.Passport',
            'app_attachments.ApplicationAttachment',
        ]
        return generic_labels + self.app_labels
