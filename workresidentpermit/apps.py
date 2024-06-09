from django.apps import AppConfig


class WorkresidentpermitConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'workresidentpermit'
    verbose_name = "Work Resident Permit Module"

    def ready(self):
        from .signals import create_production_pdf
        from .signals import create_application_decision
