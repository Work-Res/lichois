import json
import ast

from workflow.models.workflow_history import WorkflowHistory


class WorkflowHistoryService:

    @staticmethod
    def create(application, source, create_rule, result, next_activity_name):
        if application.application_status.code == next_activity_name:
            WorkflowHistory.objects.create(
                source=source.to_json(),
                create_rules=WorkflowHistoryService.to_json(create_rule),
                document_number=application.application_document.document_number,
                result=result
            )
        else:
            pass
            # print(f"application.application_status.code: {application.application_status.code}")
            # print(f"next_activity_name: {application.application_status.code}")

    @staticmethod
    def to_json(value):
        """
        Ensures the input value is converted to a JSON-compatible format.
        If the value is already JSON (dict or list), it returns it as is.
        If the value is a string, it checks if it's valid JSON and converts it.
        If the value is an object, it attempts to serialize it into JSON.
        """
        if isinstance(value, str):
            try:
                # Try to parse the string as JSON
                return ast.literal_eval(value)
            except json.JSONDecodeError:
                raise ValueError("The provided string is not valid JSON.")
        elif isinstance(value, dict) or isinstance(value, list):
            # Already a JSON-compatible structure
            return value
        else:
            try:
                # Attempt to serialize the object to JSON
                return json.loads(json.dumps(value, default=lambda o: o.__dict__))
            except (TypeError, ValueError) as e:
                raise ValueError("The provided object could not be converted to JSON.") from e
