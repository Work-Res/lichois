from django.shortcuts import get_object_or_404
from datetime import timedelta
from django.utils.timezone import now
from datetime import date
from app_checklist.models.system_parameter import SystemParameter


class SystemParameterService:

    @staticmethod
    def get_by_application_type(application_type):
        return get_object_or_404(
            SystemParameter, application_type__icontains=application_type
        )

    @staticmethod
    def calculate_expiry_date(system_parameter):
        if system_parameter.duration_type == "years":
            return system_parameter.valid_from + timedelta(
                days=365 * system_parameter.duration
            )
        elif system_parameter.duration_type == "months":
            return system_parameter.valid_from + timedelta(
                days=30 * system_parameter.duration
            )
        elif system_parameter.duration_type == "weeks":
            return system_parameter.valid_from + timedelta(
                weeks=system_parameter.duration
            )
        elif system_parameter.duration_type.lower() == "permanent":
            return None
        else:
            raise ValueError("Invalid duration type")

    @staticmethod
    def calculate_next_date(system_parameter):
        if system_parameter.duration_type == "years":
            return date.today() + timedelta(days=365 * system_parameter.duration)
        elif system_parameter.duration_type == "months":
            return date.today() + timedelta(days=30 * system_parameter.duration)
        elif system_parameter.duration_type in ["weeks", "days"]:
            return date.today() + timedelta(weeks=system_parameter.duration)
        elif system_parameter.duration_type.lower() == "permanent":
            return None
        else:
            raise ValueError("Invalid duration type")

    @staticmethod
    def create_system_parameter(data):
        SystemParameter.objects.update_or_create(
            duration_type=data.get("duration_type"),
            duration=data.get("duration"),
            application_type=data.get("application_type"),
        )
