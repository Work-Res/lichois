
from django.core.management.base import BaseCommand
from django.conf import settings

from crm_integration.config import RabbitMQConnection, RabbitMQListener


class Command(BaseCommand):
    help = 'Start listening to RabbitMQ queues'

    def handle(self, *args, **options):
        rabbitmq_connection = RabbitMQConnection(
            host=settings.RABBITMQ_HOST,
            username=settings.RABBITMQ_USERNAME,
            password=settings.RABBITMQ_PASSWORD,
            vhost=settings.RABBITMQ_VHOST  # vhost configuration
        )
        listener = RabbitMQListener(rabbitmq_connection)

        try:
            self.stdout.write(self.style.SUCCESS('Starting RabbitMQ listener...'))
            listener.start_listening()
        except KeyboardInterrupt:
            listener.stop_listening()
            self.stdout.write(self.style.WARNING('RabbitMQ listener stopped.'))