import os

from app_production.services import SystemParameterService
from app_checklist.models import SystemParameter
from app_checklist.utils import ReadJSON
from workflow.models import Task


class CreateTaskService:

    def __init__(self, request_dto):
        self.request_dto = request_dto

    def read_task_details(self):
        """
        Reads and returns the assessment rules from a JSON file.

        :return: The assessment rules as a dictionary.
        """
        try:
            file_name = "deferred_task_details.json"
            config_location = os.path.join(
                os.getcwd(), "app_checklist", "data", "tasks", file_name
            )

            reader = ReadJSON(
                file_location=self.request_dto.task_details_config_file
                or config_location
            )
            self.logger.info(
                "Successfully read rules from JSON file: %s",
                self.request_dto.task_details_config_file,
            )
            return reader.json_data()
        except Exception as e:
            self.logger.error(f"Error reading rules from JSON file: {e}")
            return {}

    def system_parameter(self):
        try:
            return SystemParameter.objects.get(
                application_type="DEFERRED_APPLICATION_DURATION"
            )
        except SystemParameter.DoesNotExist:
            pass

    def task_due_date(self):
        return SystemParameterService.calculate_next_date(self.system_parameter())

    def create_task(self):
        task_details = self.read_task_details()
        task_details.update({"office_location": None})
        task_details.update({"group_owner": None})
        task_details.update({"due_date": self.task_due_date()})
        task_details.update({"task_notes": self.request_dto.comment})
        # task_details.update({"document_number": self.request_dto.document_number})
        # task_details.update({"office_location": "Gaborone"})  # Fixme: requires Location feature implementation
        Task.objects.create(**task_details)
        return True
