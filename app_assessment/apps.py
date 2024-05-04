from django.apps import AppConfig


class AppAssessmentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_assessment'

    def ready(self):
        from .signals import run_assessment_calculation, run_assessment_calculation_handler
        run_assessment_calculation.connect(run_assessment_calculation_handler)

