from app_checklist.utils import ReadJSON


class CreateTask:

    def __init__(self, request_dto):
        self.request_dto = request_dto

    def read_task_details(self):
        """
        Reads and returns the assessment rules from a JSON file.

        :return: The assessment rules as a dictionary.
        """
        try:
            reader = ReadJSON(file_location=self.request_dto.task_details_config_file)
            self.logger.info("Successfully read rules from JSON file: %s", self.assessment_rules_file_name)
            return reader.json_data()
        except Exception as e:
            self.logger.error(f"Error reading rules from JSON file: {e}")
            return {}

    def task_due_date(self):
        pass

    def create_task(self):
        task_details = self.read_task_details()
        pass

