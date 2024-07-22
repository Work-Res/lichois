import glob
import os

from django.core.management.base import BaseCommand

from ...classes import CreateChecklistService


class Command(BaseCommand):
    help = "This is management command to create checklist data"

    # def add_arguments(self, parser):
    #     parser.add_argument(
    #         "create", type=str, help="Create system classifier for document types"
    #     )

    def handle(self, *args, **kwargs):
        # parameter = kwargs["create"]

        file_name = "attachment_documents.json"
        output_file = os.path.join(
            os.getcwd(), "app_checklist", "data", "checklist", file_name
        )
        service = CreateChecklistService(
            parent_classifier_name="classifiers",
            child_name="classifier_items",
            foreign_name="checklist_classifier",
            parent_app_label_model_name="app_checklist.checklistclassifier",
            foreign_app_label_model_name="app_checklist.checklistclassifieritem",
        )
        service.create(file_location=output_file)

        file_name = "work_resident_permit.json"

        folder_path = os.path.join(os.getcwd(), "app_checklist", "data", "workflow")
        # Get a list of all JSON files in the folder
        file_list = glob.glob(os.path.join(folder_path, "*.json"))

        for file in file_list:
            if os.path.isfile(file):
                workflow_service = CreateChecklistService(
                    parent_classifier_name="classifiers",
                    child_name="classifier_items",
                    foreign_name="classifier",
                    parent_app_label_model_name="app_checklist.classifier",
                    foreign_app_label_model_name="app_checklist.classifieritem",
                )
                workflow_service.create(file_location=file)

        file_name = "office_locations.json"
        office_file = os.path.join(
            os.getcwd(), "app_checklist", "data", "offices", file_name
        )
        service_office = CreateChecklistService(
            parent_classifier_name="Location",
            child_name="offices",
            foreign_name="office_location_classifier",
            parent_app_label_model_name="app_checklist.officelocationclassifier",
            foreign_app_label_model_name="app_checklist"
            ".officelocationclassifieritem",
        )
        service_office.create(file_location=office_file)

        self.stdout.write(self.style.SUCCESS("Create or Update document types"))
