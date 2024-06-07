import os

from unittest.mock import patch

from django.test import TestCase


from app_checklist.classes import CreateChecklistService
from app_checklist.models import Classifier, ClassifierItem, OfficeLocationClassifier, OfficeLocationClassifierItem, \
    ChecklistClassifier, ChecklistClassifierItem


class TestCreateClassifier(TestCase):

    def test_create_or_update_classifier_and_classifier_items(self):
        file_name = "attachment_documents.json"
        output_file = os.path.join(os.getcwd(), "app_checklist", "data", file_name)

        service = CreateChecklistService(parent_classifier_name="classifiers", child_name="classifier_items",
                                         foreign_name="classifier",
                                         parent_app_label_model_name="app_checklist.classifier",
                                         foreign_app_label_model_name="app_checklist.classifieritem")
        service.create(file_location=output_file)

        classifiers = Classifier.objects.all()
        self.assertEqual(len(classifiers), 4)
        classifier_items = ClassifierItem.objects.all()
        self.assertEqual(len(classifier_items), 14)

    def test_check_create_offices(self):
        file_name = "office_locations.json"
        output_file = os.path.join(os.getcwd(), "app_checklist", "data", "offices", file_name)

        service = CreateChecklistService(parent_classifier_name="Location", child_name="offices",
                                         foreign_name="office_location_classifier",
                                         parent_app_label_model_name="app_checklist.officelocationclassifier",
                                         foreign_app_label_model_name="app_checklist.officelocationclassifieritem")
        service.create(file_location=output_file)

        classifiers = OfficeLocationClassifier.objects.all()
        self.assertEqual(len(classifiers), 1)
        classifier_items = OfficeLocationClassifierItem.objects.all()
        self.assertEqual(len(classifier_items), 3)

    def test_check_create_when_creating_attachments(self):
        file_name = "attachment_documents.json"
        output_file = os.path.join(os.getcwd(), "app_checklist", "data", "checklist", file_name)

        service = CreateChecklistService(parent_classifier_name="classifiers", child_name="classifier_items",
                                         foreign_name="checklist_classifier",
                                         parent_app_label_model_name="app_checklist.checklistclassifier",
                                         foreign_app_label_model_name="app_checklist.checklistclassifieritem")
        service.create(file_location=output_file)

        classifiers = ChecklistClassifier.objects.all()
        self.assertEqual(len(classifiers), 1)
        classifier_items = ChecklistClassifierItem.objects.all()
        self.assertEqual(len(classifier_items), 6)
