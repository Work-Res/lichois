# form_submission_handler.py
import logging

from django.apps import apps

from .model_repository import ModelRepository
from .model_service import ModelService


class FormSubmissionHandler:
    def __init__(self, data):
        self.data = data
        self.model_data = {}
        self.errors = {}
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

    def collect_model_data(self):
        for key, value in self.data.items():
            try:
                parts = key.split("_")
                app_name_parts = []
                model_name = None
                field_name_parts = []

                for part in parts:
                    if part[0].isupper():
                        model_name = part
                        field_name_parts = parts[parts.index(part) + 1 :]
                        break
                    else:
                        app_name_parts.append(part)

                app_name = "_".join(app_name_parts)
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

                model_cls = apps.get_model(app_name, model_name)
                repository = ModelRepository(model_cls)
                service = ModelService(repository)

                instance, created = service.process_data(fields)
                print(f"Instance: {instance}, Created: {created}")

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
