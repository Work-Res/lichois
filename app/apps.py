from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    verbose_name = "Application Framework Module"
    name = "app"

    def ready(self):
        import app.signals
        from app.identifiers.identifier_scan_register import registrar

        registrar.scan_and_register_identifier_config_classes()
        print("Registered classes: ", registrar.registered_identifier_config_classes)
