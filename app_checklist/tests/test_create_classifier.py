import os
import pytest

pytestmark = pytest.mark.django_db

from app_checklist.classes import CreateChecklist
from app_checklist.models import Classifier, ClassifierItem


class TestCreateClassifier:

    def test_create_or_update_classifier_and_classifier_items(self):
        file_name = "attachment_documents.json"
        output_file = os.path.join(os.getcwd(), "app_checklist", "data", file_name)
        create = CreateChecklist()
        create.create(file_location=output_file)
        assert create.classifier is not None
        assert create.classifier.id is not None
        assert Classifier.objects.count() == 1
        assert ClassifierItem.objects.count() == len(create.classifier_items)
