# utils.py
from django.apps import apps


def get_service_registry():
    app_config = apps.get_app_config("app_production")
    return app_config.service_registry
