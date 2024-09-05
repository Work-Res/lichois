from django.apps import AppConfig


class CitizenshipConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'citizenship'
    verbose_name = 'Citizenship'
    admin_site_name = 'citizenship_admin'

    def ready(self):
        from .signals import handle_conflict_duration_completed
        from .handlers import production_decision_post_save_on_verfication_handler
        from .handlers import production_decision_post_save_handler
        from .handlers import production_decision_minister_decision_handler

