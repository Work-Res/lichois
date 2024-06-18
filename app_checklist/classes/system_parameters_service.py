from django.shortcuts import get_object_or_404
from datetime import timedelta
from django.utils.timezone import now
from .models import SystemParameter

class SystemParameterService:
    
    @staticmethod
    def get_by_application_type(application_type):
        return get_object_or_404(SystemParameter, application_typea__icontains=application_type)

    @staticmethod
    def calculate_expiry_date(system_parameter):
        valid_from = system_parameter.valid_from or now().date()
        if system_parameter.duration_type == 'years':
            expiry_date = valid_from + timedelta(days=365 * system_parameter.duration)
        elif system_parameter.duration_type == 'months':
            expiry_date = valid_from + timedelta(days=30 * system_parameter.duration)
        elif system_parameter.duration_type == 'weeks':
            expiry_date = valid_from + timedelta(weeks=system_parameter.duration)
        else:
            raise ValueError('Invalid duration_type')
        
        return expiry_date
