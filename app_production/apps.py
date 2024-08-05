from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app_production"

    def ready(self):
        from .classes import ProductionPermitTemplateSearcher

        searcher = ProductionPermitTemplateSearcher()
        searcher.search_and_create_template()
