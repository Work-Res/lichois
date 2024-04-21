from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):

    name = 'visa'
    verbose_name = 'Visa'
    admin_site_name = 'visa_admin'
