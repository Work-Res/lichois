import logging

from django.apps import apps
from django.core.exceptions import MultipleObjectsReturned


from app_checklist.utils import ReadJSON

from .pre_pupolation_model_definition import PrepopulationConfiguration, BaseConfiguration
"""
TODO: NO TESTS, and more tests are required.
"""


class PrePupolation(object):

    def __init__(self, old_application_version=None, new_application_version=None, process_name=None, configuration_location=None,
                 filter_data=None):
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
        self.configuration()
        for prepopulation_model_definition in self.prepopulation_configuration.models:
            app_model = self.get_model_by_label(prepopulation_model_definition.model)
            self.create_model_obj(app_model, prepopulation_model_definition.filters)

    def get_model_by_label(self, model_str):
        try:
            app_label, model_name = model_str.split('.')
            model = apps.get_model(app_label, model_name)
            return model
        except LookupError:
            print(f"Model '{model_name}' in app '{app_label}' not found.")

    def create_model_obj(self, model_cls, filter):
        try:
            model_obj = model_cls.objects.get(**self.update_filter(filter))
            self.update_model_for_core_module(model_obj)
        except model_cls.DoesNotExit:
            self.logger.debug(f"PrepopulationError: model does not exist {model_obj} - {self.update_filter}")
        except MultipleObjectsReturned:
            model_objs = model_cls.objects.filter(**self.update_filter(filter))
            for model_obj in model_objs:
                self.update_model_for_core_module(model_obj)

    def update_model_for_core_module(self, model_obj):
        model_obj.document_number = self.new_application_version.application.application_document.document_number
        model_obj.application_verison = self.new_application_version
        model_obj.save()

    def update_filter(self, filter):
        updated_dict = {}
        for key in filter:
            updated_dict.update({key: self.filter_data.get(key)})
        return updated_dict
