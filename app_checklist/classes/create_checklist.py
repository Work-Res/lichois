import copy

from app_checklist.utils import ReadJSON
from app_checklist.models import Classifier, ClassifierItem


class CreateChecklist:
    """
    Loads json file for document types, and create records in the database.
    """

    def __init__(self):
        self.classifier = None
        self.classifier_items = []

    def create(self, file_location=None):
        reader = ReadJSON(file_location=file_location)
        data = reader.json_data()
        for classifier_key, classifier_value in data["classifiers"].items():
            _data = copy.copy(classifier_value)
            obj, created = self.create_classifier(_data)
            created_classifier = obj if obj else created
            self.create_classifier_items(classifier_value['classifier_items'], created_classifier)

    def create_classifier_items(self, data, classifier):
        for item in data:
            item.update({'classifier': classifier})
            classifier_item = ClassifierItem.objects.update_or_create(
                code=item['code'],
                defaults=item
            )
            self.classifier_items.append(classifier_item)

    def create_classifier(self, data):
        del data['classifier_items']
        obj, created = Classifier.objects.update_or_create(
            code=data['code'],
            defaults=data
        )
        return obj, created
