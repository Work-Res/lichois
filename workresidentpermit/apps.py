from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "workresidentpermit"
    verbose_name = "Work Resident Permit Module"

    def ready(self):
        from .signals import create_application_final_decision_by_security_clearance
        from .signals import create_application_final_decision_by_commissioner_decision
        from .signals import create_application_final_decision_by_minister_decision
        from board.signals import create_application_decision
        from .signals import create_production_permit_record
