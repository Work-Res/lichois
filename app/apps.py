from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    verbose_name = "Application Framework Module"
    name = 'app'

    def ready(self):
        import app.signals
