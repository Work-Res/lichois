import os

from unittest.mock import patch

from django.test import TestCase


from app_checklist.classes import CreateChecklist
from app_checklist.models import Classifier, ClassifierItem


class TestCreateClassifier(TestCase):

    def test_create_or_update_classifier_and_classifier_items(self):
        file_name = "attachment_documents.json"
        output_file = os.path.join(os.getcwd(), "app_checklist", "data", file_name)
        create = CreateChecklist()
        create.create(file_location=output_file)
        classifiers = Classifier.objects.all()
        self.assertEqual(len(classifiers), 4)
        classifier_items = ClassifierItem.objects.all()
        self.assertEqual(len(classifier_items), 13)
