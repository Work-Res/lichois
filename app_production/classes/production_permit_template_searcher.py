from app_checklist.utils.read_json import ReadJSON
from .directory_searcher import DirectorySearcher
from .json_file_searcher import JsonFileSearcher
from app_production.services import SystemParameterService


class ProductionPermitTemplateSearcher:
    def __init__(self):
        directory_searcher = DirectorySearcher("production")
        self.directories = directory_searcher.search_directories_in_apps()
        json_file_searcher = JsonFileSearcher(self.directories)
        self.json_files = json_file_searcher.search_json_files_in_directories()

    def search_and_create_template(self):
        for app_name, files in self.json_files.items():
            for file in files:
                reader = ReadJSON(file_location=file)
                data = reader.json_data()
                print(f"Creating system parameter for {file} from {data}")
                SystemParameterService.create_system_parameter(data)

    def display_results(self):
        if self.directories:
            print("Found directories:")
            for app_name, directory in self.directories.items():
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
