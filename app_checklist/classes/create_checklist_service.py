import logging
import copy

from django.apps import apps
from typing import List, Dict, Any

from app_checklist.utils import ReadJSON

logger = logging.getLogger(__name__)


class CreateChecklistService:
    """
    Loads json file for document types, and create records in the database.
    """

    def __init__(self, parent_classifier_name: str = None, child_name: str = None, foreign_name: str = None,
                 parent_app_label_model_name: str = None, foreign_app_label_model_name: str = None):
        self.classifier = None
        self.classifier_items = []
        self.parent_classifier_name = parent_classifier_name
        self.child_name = child_name
        self.foreign_name = foreign_name
        self.parent_app_label_model_name = parent_app_label_model_name
        self.foreign_app_label_model_name = foreign_app_label_model_name

    def create(self, file_location=None):
        reader = ReadJSON(file_location=file_location)
        data = reader.json_data()
        for classifier_key, classifier_value in data[self.parent_classifier_name].items():
            _data = copy.copy(classifier_value)
            obj, created = self.create_classifier(_data)
            created_classifier = obj if obj else created
            self.create_classifier_items(classifier_value[self.child_name], created_classifier)

    def create_classifier_items(self, data: List[Dict[str, Any]], classifier: str) -> None:
        app_label, model_name = self.foreign_app_label_model_name.split('.')
        model = self.get_model_by_app_label_and_model_name(app_label, model_name)

        for item in data:
            item[self.foreign_name] = classifier

            classifier_item, created = model.objects.update_or_create(
                code=item['code'],
                defaults=item
            )

            action = "created" if created else "updated"
            logger.info(f"Classifier item {action}: {classifier_item}")

            self.classifier_items.append(classifier_item)

    def create_classifier(self, data):
        del data[self.child_name]
        app_label, model_name = self.parent_app_label_model_name.split('.')
        model = self.get_model_by_app_label_and_model_name(app_label, model_name)
        obj, created = model.objects.update_or_create(
            code=data['code'],
            defaults=data
        )
        return obj, created

    def get_model_by_app_label_and_model_name(self, app_label, model_name):
        try:
            model = apps.get_model(app_label, model_name)
            return model
        except LookupError:
            return None
