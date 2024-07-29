import os
import logging
from django.apps import apps


class DirectorySearcher:
    def __init__(self, target_directory_name):
        self.target_directory_name = target_directory_name
        self.results = {}

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
