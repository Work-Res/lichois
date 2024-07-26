import logging
import copy

from django.apps import apps
from typing import List, Dict, Any


from app_checklist.utils import ReadJSON
from django.core.exceptions import MultipleObjectsReturned


class CreateChecklistService:
    """
    Loads json file for document types, and create records in the database.
    """

    def __init__(
        self,
        parent_classifier_name: str = None,
        child_name: str = None,
        foreign_name: str = None,
        parent_app_label_model_name: str = None,
        foreign_app_label_model_name: str = None,
    ):
        self.classifier = None
        self.classifier_items = []
        self.parent_classifier_name = parent_classifier_name
        self.child_name = child_name
        self.foreign_name = foreign_name
        self.parent_app_label_model_name = parent_app_label_model_name
        self.foreign_app_label_model_name = foreign_app_label_model_name
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

    def create(self, file_location=None):
        reader = ReadJSON(file_location=file_location)
        data = reader.json_data()
        for classifier_key, classifier_value in data[
            self.parent_classifier_name
        ].items():
            _data = copy.copy(classifier_value)
            created_classifier = self.create_or_update_classifier(_data)
            self.create_classifier_items(
                classifier_value[self.child_name], created_classifier
            )

    def create_classifier_items(
        self, data: List[Dict[str, Any]], classifier: str
    ) -> None:
        app_label, model_name = self.foreign_app_label_model_name.split(".")
        model = self.get_model_by_app_label_and_model_name(app_label, model_name)

        for item in data:
            item[self.foreign_name] = classifier
            lookup_kwargs = {self.foreign_name: classifier, "code": item["code"]}
            try:
                obj = model.objects.get(**lookup_kwargs)
                self.logger.debug(f"Existing object found: {obj}")
                try:
                    if item["application_type"] not in obj.application_type:
                        obj.application_type = (
                            f"{obj.application_type},{item['application_type']}"
                        )
                        obj.save()
                        self.logger.info(
                            f"Updated object {obj.id} with new application type: {obj.application_type}"
                        )
                    else:
                        logging.debug(f"No update needed for object {obj.id}")
                    return obj
                except Exception:
                    return obj
            except model.DoesNotExist:
                classifier_item, created = model.objects.update_or_create(
                    **lookup_kwargs, defaults=item
                )
                action = "created" if created else "updated"
                self.logger.info(f"Classifier item {action}: {classifier_item}")
            except MultipleObjectsReturned:
                self.logger.error(
                    f"Multiple objects returned for lookup_kwargs: {lookup_kwargs}"
                )

            self.classifier_items.append(classifier_item)

    def update_classifier(self, data: dict, model):
        pass

    def create_or_update_classifier(self, data):
        # Remove child_name from data dictionary
        data.pop(self.child_name, None)
        app_label, model_name = self.parent_app_label_model_name.split(".")
        model = self.get_model_by_app_label_and_model_name(app_label, model_name)

        self.logger.info(
            f"Creating or updating classifier: {self.parent_app_label_model_name}"
        )
        try:
            obj = model.objects.get(code__iexact=data["code"])
            self.logger.debug(f"Existing object found: {obj}")
            try:
                if data["process_name"] not in obj.process_name:
                    obj.process_name = f"{obj.process_name},{data['process_name']}"
                    obj.save()
                    self.logger.info(
                        f"Updated object {obj.id} with new process_name: {obj.process_name}"
                    )
                else:
                    self.logger.debug(f"No update needed for object {obj.id}")
                return obj
            except Exception:
                return obj
        except model.DoesNotExist:
            new_obj = model.objects.create(**data)
            self.logger.info(f"Created new object with id: {new_obj.id}")
            return new_obj
        except Exception as e:
            self.logger.error(f"Error in create_or_update_classifier: {e}")
            raise e

    def get_model_by_app_label_and_model_name(self, app_label, model_name):
        try:
            model = apps.get_model(app_label, model_name)
            return model
        except LookupError:
            return None
