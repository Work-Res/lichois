from django.apps import AppConfig


class TravelConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "travel"
    verbose_name = "Travel Module"

    def ready(self):
        import travel.signals
