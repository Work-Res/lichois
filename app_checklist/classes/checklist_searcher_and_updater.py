import os
import logging
from django.apps import apps
from app_checklist.classes import CreateChecklistService


class ChecklistSearcherAndUpdater:

    def __init__(self, target_directory_name):
        self.target_directory_name = target_directory_name
        self.results = {}
        self.json_files = {}

    def search_directories_in_apps(self):
        try:
            for app in apps.get_app_configs():
                app_path = app.path
                self.recursive_search(app_path, app.name)

            if not self.results:
                logging.warning(
                    f"No '{self.target_directory_name}' directories found in any app."
                )
        except Exception as e:
            logging.error(f"Error while searching directories in apps: {e}")

        return self.results

    def recursive_search(self, current_path, app_name):
        try:
            for root, dirs, files in os.walk(current_path):
                if self.target_directory_name in dirs:
                    target_path = os.path.join(root, self.target_directory_name)
                    self.results[app_name] = target_path
                    logging.info(
                        f"Found directory '{self.target_directory_name}' in app '{app_name}' at '{target_path}'"
                    )
                    return
        except Exception as e:
            logging.error(f"Error while searching directories in '{current_path}': {e}")

    def search_json_files_in_directories(self):
        try:
            for app_name, directory in self.results.items():
                json_files = [f for f in os.listdir(directory) if f.endswith(".json")]
                if json_files:
                    self.json_files[app_name] = [
                        os.path.join(directory, f) for f in json_files
                    ]
                    logging.info(
                        f"Found JSON files in '{directory}' for app '{app_name}'"
                    )
                else:
                    logging.info(
                        f"No JSON files found in '{directory}' for app '{app_name}'"
                    )

            if not self.json_files:
                logging.warning("No JSON files found in any of the directories.")
        except Exception as e:
            logging.error(f"Error while searching for JSON files in directories: {e}")

        return self.json_files

    def update_checklist(self):
        """Scans all registered apps, and look for target json file.
        :return:
        """
        self.search_directories_in_apps()
        self.search_json_files_in_directories()
        for app_name, json_files in self.json_files.items():
            for new_file in json_files:
                checklist_service = CreateChecklistService(
                    parent_classifier_name="classifiers",
                    child_name="classifier_items",
                    foreign_name="checklist_classifier",
                    parent_app_label_model_name="app_checklist.checklistclassifier",
                    foreign_app_label_model_name="app_checklist.checklistclassifieritem",
                )
                checklist_service.create(file_location=new_file)

    def update_workflow(self):
        """Scans all registered apps, and look for target json file.
        :return:
        """
        self.search_directories_in_apps()
        self.search_json_files_in_directories()
        for app_name, json_files in self.json_files.items():
            for new_file in json_files:
                try:
                    workflow_service = CreateChecklistService(
                        parent_classifier_name="classifiers",
                        child_name="classifier_items",
                        foreign_name="classifier",
                        parent_app_label_model_name="app_checklist.classifier",
                        foreign_app_label_model_name="app_checklist.classifieritem",
                    )
                    workflow_service.create(file_location=new_file)
                except Exception as e:
                    logging.error(
                        f"An error occurred while creating a workflow file, {str(e)} {new_file}"
                    )
        self.display_results()

    def display_results(self):
        if self.results:
            for app_name, directory in self.results.items():
                print(f"{app_name}: {directory}")
        else:
            print(f"No '{self.target_directory_name}' directories found in any app.")

    def display_json_files(self):
        if self.json_files:
            print("\nFound JSON files:")
            for app_name, files in self.json_files.items():
                print(f"{app_name}:")
                for file in files:
                    print(f"  - {file}")
        else:
            print("No JSON files found in the directories.")
