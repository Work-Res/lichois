from django.apps import AppConfig as BaseAppConfig
from django.conf import settings

from crm_integration.config import RabbitMQConfig


class AppConfig(BaseAppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "crm_integration"

    def ready(self):
        if settings.USE_RABBITMQ:  # Conditional to ensure RabbitMQ is only set up when needed
            rabbitmq_config = RabbitMQConfig(
                host=settings.RABBITMQ_HOST,
                username=settings.RABBITMQ_USERNAME,
                password=settings.RABBITMQ_PASSWORD,
                vhost=settings.RABBITMQ_VHOST  # vhost configuration
            )
            rabbitmq_config.setup()
