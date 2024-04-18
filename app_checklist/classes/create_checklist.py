from app_checklist.utils import ReadJSON
from app_checklist.models import Classifier, ClassifierItem


class CreateChecklist:
    """
    Loads json file for document types, and create records in the database.
    TODO: Extend to support multiple classifiers
    """

    def __init__(self):
        self.classifier = None
        self.classifier_items = []

    def create(self, file_location=None):
        reader = ReadJSON(file_location=file_location)
        data = reader.json_data()
        obj, created = self.create_classifier(data['classifiers']['attachment_documents'])
        self.classifier = obj if obj is not None else created
        data_items = reader.json_data()
        self.create_classifier_items(data_items['classifiers']['attachment_documents']['classifier_items'])

    def create_classifier_items(self, data):
        for item in data:
            item.update({'classifier': self.classifier})
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
