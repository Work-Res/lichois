import logging

from django.apps import apps
from django.db.models import Model
from django.db import transaction
from typing import Optional

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from typing import Type, Any, Dict

from app_checklist.utils import ReadJSON

from .pre_pupolation_model_definition import PrepopulationConfiguration, BaseConfiguration
"""
TODO: NO TESTS, and more tests are required.
"""
from app.models import ApplicationVersion


class PrePopulationService(object):

    def __init__(self, old_application_version: ApplicationVersion, new_application_version: ApplicationVersion,
                 process_name=None, configuration_location=None, filter_data=None):
        self.logger = logging.getLogger(__name__)
        self.process_name = process_name
        self.configuration_location = configuration_location
        self.prepopulation_configuration = None
        self.filter_data = filter_data
        self.old_application_version = old_application_version
        self.new_application_version = new_application_version

    def configuration(self):
        self.prepopulation_configuration = BaseConfiguration.from_dict(
            PrepopulationConfiguration, ReadJSON(self.configuration_location).json_data())

    def prepupoluate(self):
        success = False
        try:
            self.configuration()
            for prepopulation_model_definition in self.prepopulation_configuration.models:
                app_model = self.get_model_by_label(prepopulation_model_definition.get("model"))
                self.create_model_obj(app_model, prepopulation_model_definition.get("filters"))
            success = True
        except Exception as e:
            print("An error, ", e)
            self.logger.debug(f"An error occurred, got {e}")
        return success

    def get_model_by_label(self, model_str: str) -> Optional[Model]:
        """
        Retrieve a Django model class based on its app label and model name.

        Args:
            model_str (str): The model string in the format 'app_label.model_name'.

        Returns:
            Optional[Model]: The Django model class if found, otherwise None.
        """
        try:
            app_label, model_name = model_str.split('.')
            model = apps.get_model(app_label, model_name)
            return model
        except LookupError:
            self.logger.error(f"Model '{model_name}' in app '{app_label}' not found.")
        except ValueError:
            self.logger.error(f"Invalid model string '{model_str}'. Expected format 'app_label.model_name'.")
        return None

    @transaction.atomic
    def create_model_obj(self, model_cls: Type[Any], filter: Dict[str, Any]) -> None:
        filter_params = self.update_filter(filter)
        try:
            model_obj = model_cls.objects.get(**filter_params)
            self.update_model_for_core_module(model_obj)
        except ObjectDoesNotExist:
            self.logger.debug(f"PrepopulationError: model does not exist for filter {filter_params}")
            raise
        except MultipleObjectsReturned:
            self.logger.warning(f"Multiple objects returned for filter {filter_params}. Updating all.")
            model_objs = model_cls.objects.filter(**filter_params)
            for model_obj in model_objs:
                self.update_model_for_core_module(model_obj)
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {str(e)}")
            raise

    def update_model_for_core_module(self, model_obj: Any) -> None:

        try:
            new_app_version = self.new_application_version
            new_doc_number = new_app_version.application.application_document.document_number
            model_obj.document_number = new_doc_number
            model_obj.application_version = new_app_version
            model_obj.save()
            self.logger.info(f"Model {model_obj} updated successfully with new document number {new_doc_number} "
                             f"and application version {new_app_version}.")
        except AttributeError as e:
            self.logger.error(f"Attribute error occurred: {str(e)}")
        except Exception as e:
            self.logger.error(f"An unexpected error occurred while updating the model: {str(e)}")

    def update_filter(self, filter):
        updated_dict = {}
        for key in filter:
            updated_dict.update({key: self.filter_data.get(key)})
        return updated_dict
