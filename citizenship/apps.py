from django.apps import AppConfig


class CitizenshipConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'citizenship'
    verbose_name = 'Citizenship'
    admin_site_name = 'citizenship_admin'
