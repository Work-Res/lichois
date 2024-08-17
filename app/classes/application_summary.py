import re
from django.apps import apps
from django.core.exceptions import FieldDoesNotExist, FieldError, ObjectDoesNotExist
from django.db.models import ForeignKey, ManyToManyField, QuerySet
from django.forms import model_to_dict


class ApplicationSummary:
    def __init__(self, document_number, app_labels):
        """Initialize the ApplicationSummary with a document number and application labels."""
        self.document_number = document_number
        self.app_labels = app_labels

    def data(self):
        """Generate a summary of the application data."""
        summary = {}
        for app_label in self.get_app_labels():
            model_instance = self.get_model_instance(app_label)
            if model_instance:
                model_name = apps.get_model(app_label).__name__
                snake_case_model_name = self.to_snake_case(model_name)
                summary[snake_case_model_name] = self.serialize_model_instance(
                    model_instance
                )
        return summary

    def get_model_instance(self, app_label):
        """Get the model instance based on the app label and document number."""
        model_cls = apps.get_model(app_label)
        print(f"Getting model instance for {model_cls}")
        return self._get_model_instance_recursive(model_cls)

    def _get_model_instance_recursive(self, model_cls, traversed_models=None):
        """Recursively get the model instance based on the document number."""
        if traversed_models is None:
            traversed_models = set()

        try:
            # Attempt to filter using document_number directly
            return model_cls.objects.get(document_number=self.document_number)
        except (FieldError, model_cls.DoesNotExist):
            # Add the current model to traversed models to avoid infinite loops
            traversed_models.add(model_cls)

            # Fallback to check for ForeignKey relationships with document_number
            for field in model_cls._meta.get_fields():
                if isinstance(field, ForeignKey):
                    related_model = field.related_model
                    if related_model not in traversed_models:
                        try:
                            related_instance = self._get_model_instance_recursive(
                                related_model, traversed_models
                            )
                            if related_instance:
                                return model_cls.objects.get(
                                    **{field.name: related_instance}
                                )
                        except ObjectDoesNotExist:
                            continue
        except FieldDoesNotExist:
            return None
        return None

    def serialize_model_instance(self, model_instance):
        """Serialize a model instance to a dictionary."""
        serialized_data = {}
        for field in model_instance._meta.get_fields():
            field_name = field.name
            try:
                if isinstance(field, ForeignKey):
                    # Handle ForeignKey relationships
                    related_instance = getattr(model_instance, field_name)
                    if related_instance:
                        serialized_data[field_name] = self.serialize_related_instance(
                            related_instance
                        )
                    else:
                        serialized_data[field_name] = None
                elif isinstance(field, ManyToManyField):
                    # Handle ManyToManyField relationships
                    related_manager = getattr(model_instance, field_name)
                    serialized_data[field_name] = [
                        self.serialize_related_instance(instance)
                        for instance in related_manager.all()
                    ]
                elif hasattr(getattr(model_instance, field_name), "all"):
                    # Handle reverse ForeignKey relationships
                    related_manager = getattr(model_instance, field_name)
                    serialized_data[field_name] = [
                        self.serialize_related_instance(instance)
                        for instance in related_manager.all()
                    ]
                else:
                    # Handle other fields normally
                    serialized_data[field_name] = getattr(model_instance, field_name)
            except AttributeError as e:
                # Handle the case where an attribute doesn't exist on the model instance
                print(f"Error accessing field '{field_name}' on {model_instance}: {e}")
                # serialized_data[field_name] = None

        return serialized_data

    def serialize_related_instance(self, related_instance):
        """Serialize a related instance (ForeignKey or queryset) to a dictionary."""

        def instance_to_dict(instance):
            """Convert a model instance to a dictionary."""
            if hasattr(instance, "to_dict"):
                print("Using custom to_dict method")
                return instance.to_dict()
            return model_to_dict(
                instance, fields=[field.name for field in instance._meta.fields]
            )

        if isinstance(related_instance, QuerySet):
            # Handle queryset of related instances
            return [instance_to_dict(instance) for instance in related_instance]
        else:
            # Handle ForeignKey relationships
            return instance_to_dict(related_instance)

    @staticmethod
    def to_snake_case(camel_str):
        """Convert a CamelCase string to snake_case."""
        return re.sub("([a-z0-9])([A-Z])", r"\1_\2", camel_str).lower()

    def get_app_labels(self):
        """Get the list of app labels to be used in the summary."""
        generic_labels = [
            "app_personal_details.Person",
            "app_address.ApplicationAddress",
            "app_contact.ApplicationContact",
            "app_personal_details.Passport",
            "app.Application",
            "app.ApplicationVerification",
            "app.SecurityClearance",
            "app_personal_details.Education",
            "base_module.Spouse",
            "base_module.Child",
        ]
        return generic_labels + self.app_labels
