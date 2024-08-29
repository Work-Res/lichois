from ast import mod
from django.apps import apps
import logging
from django.db import transaction
from ..api.serializers import create_model_serializer

from identifier.non_citizen_identifier import NonCitizenIdentifier


class NonCitizenProfileDeserializer:

    def __init__(self, data):
        self.data = data
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.errors = {}
        self.model_data = {}
        self.app_name = "non_citizen_profile"
        self.identifier = self.make_new_identifier()

    def deserialize(self):
        return self.data

    def collect_model_data(self):
        for key, value in self.data.items():
            try:
                parts = key.split("_")
                model_name = None
                field_name_parts = []

                for part in parts:
                    if part[0].isupper():
                        model_name = part
                        i = parts.index(part) + 1
                        field_name_parts = parts[i:]
                        break

                field_name = "_".join(field_name_parts)

                if model_name not in self.model_data:
                    self.model_data[model_name] = {"fields": {}}
                self.model_data[model_name]["fields"][field_name] = value

            except Exception as e:
                self.logger.error(f"Error processing key '{key}': {e}")
                self.errors[key] = str(e)

    @transaction.atomic
    def handle(self):
        self.collect_model_data()
        for model_name, data in self.model_data.items():
            try:
                fields = data["fields"]
                fields["non_citizen_identifier"] = self.identifier
                self.logger.debug(f"Fields: {fields}")
                model_cls = apps.get_model(self.app_name, model_name)
                serializer = create_model_serializer(model_cls)(data=fields)
                if serializer.is_valid():
                    obj, _ = model_cls.objects.get_or_create(
                        defaults=serializer.validated_data
                    )
                else:
                    self.logger.error(serializer.errors)
                    self.errors[model_name] = serializer.errors

            except LookupError:
                self.logger.error(
                    f"Model '{model_name}' not found in app '{self.app_name}'."
                )
                self.errors[model_name] = (
                    f"Model '{model_name}' not found in app '{self.app_name}'."
                )
            except ValueError as e:
                self.logger.error(f"Error processing model '{model_name}': {e}")
                self.errors[model_name] = e.args[0]
            except Exception as e:
                self.logger.error(f"Error processing model '{model_name}': {e}")
                self.errors[model_name] = str(e)
        return self.errors

    def make_new_identifier(self):
        """Returns a new and unique identifier.

        Override this if needed.
        """
        non_citizen_identifier = NonCitizenIdentifier(
            dob=self.data["PersonalDetails_dob"],
            label="non_citizen_identifier",
        )
        return non_citizen_identifier.identifier
