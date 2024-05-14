from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):
    name = 'authentication'  # This should match the name of your app module
    verbose_name = 'User Authentication'  # Optional, human-readable name for the app
    app_label = 'authentication'
