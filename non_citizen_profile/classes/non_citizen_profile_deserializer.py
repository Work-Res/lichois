from django.apps import apps
import logging
from ..api.serializers import create_model_serializer

# from identifier.non_citizen_identifier import NonCitizenIdentifier


class NonCitizenProfileDeserializer:

    def __init__(self, data):
        self.data = data
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.errors = {}

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

                app_name = "non_citizen_profile"
                field_name = "_".join(field_name_parts)

                if model_name not in self.model_data:
                    self.model_data[model_name] = {"app_name": app_name, "fields": {}}
                self.model_data[model_name]["fields"][field_name] = value

            except Exception as e:
                self.logger.error(f"Error processing key '{key}': {e}")
                self.errors[key] = str(e)

    def handle(self):
        self.collect_model_data()
        for model_name, data in self.model_data.items():
            try:
                app_name = data["app_name"]
                fields = data["fields"]
                identifier = self.make_new_identifier()
                fields["non_citizen_identifier"] = identifier

                serializer = create_model_serializer(self.repository.model_cls)(
                    data=fields
                )
                if serializer.is_valid():
                    model_cls = apps.get_model(app_name, model_name)

                    obj, _ = model_cls.objects.get_or_create(
                        defaults=serializer.validated_data
                    )
                    print(f"Instance: {obj}, Created: {obj}")
                else:
                    self.logger.error(serializer.errors)
                    self.errors[model_name] = serializer.errors

            except LookupError:
                self.logger.error(
                    f"Model '{model_name}' not found in app '{app_name}'."
                )
                self.errors[model_name] = (
                    f"Model '{model_name}' not found in app '{app_name}'."
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
        # non_citizen_identifier = NonCitizenIdentifier(
        #     dob=self.data["Address_dob"], label="non_citizen_identifier"
        # )
        # return non_citizen_identifier.identifier
