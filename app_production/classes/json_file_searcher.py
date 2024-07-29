import os
import logging


class JsonFileSearcher:
    def __init__(self, directories):
        self.directories = directories
        self.json_files = {}

    def search_json_files_in_directories(self):
        try:
            for app_name, directory in self.directories.items():
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
