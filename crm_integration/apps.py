import logging

from django.apps import AppConfig as BaseAppConfig
from django.conf import settings

from crm_integration.config import RabbitMQConfig, RabbitMQConnection

logger = logging.getLogger('rabbitmq_setup')


class AppConfig(BaseAppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "crm_integration"

    def ready(self):
        if settings.USE_RABBITMQ:  # Conditional to ensure RabbitMQ is only set up when needed
            try:
                # Establish the connection to RabbitMQ
                rabbitmq_connection = RabbitMQConnection(
                    host=settings.RABBITMQ_HOST,
                    username=settings.RABBITMQ_USERNAME,
                    password=settings.RABBITMQ_PASSWORD,
                    vhost=settings.RABBITMQ_VHOST  # vhost configuration
                )

                # Pass the connection to the config setup
                rabbitmq_config = RabbitMQConfig(rabbitmq_connection)
                rabbitmq_config.setup()
                logger.debug("Connected successfully.")
            except Exception as e:
                # Log an error if the RabbitMQ setup fails
                logger.error(f"Failed to set up RabbitMQ in AppConfig: {e}")
