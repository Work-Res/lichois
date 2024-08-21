import logging
from crm_integration.config import RabbitMQConnection
from crm_integration.exceptions import RabbitMQServiceError
from crm_integration.producer import RabbitMQProducer
from django.conf import settings
import pika.exceptions

logger = logging.getLogger('rabbitmq_service')


class RabbitMQService:

    def __init__(self, queue_name, exchange_key, message=None):
        self.message = message
        self.exchange_key = exchange_key
        self.queue_name = queue_name
        self.rabbitmq_connection = None
        self.producer = None

        try:
            # Establish RabbitMQ connection
            self.rabbitmq_connection = RabbitMQConnection(
                host=settings.RABBITMQ_HOST,
                username=settings.RABBITMQ_USERNAME,
                password=settings.RABBITMQ_PASSWORD,
                vhost=settings.RABBITMQ_VHOST  # vhost configuration
            )
            # Initialize producer
            self.producer = RabbitMQProducer(
                connection=self.rabbitmq_connection, queue_name=self.queue_name,
                exchange_key=self.exchange_key
            )
            logger.info(
                f"Initialized RabbitMQService for queue: {self.queue_name} and exchange key: {self.exchange_key}")

        except pika.exceptions.AMQPConnectionError as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            raise RabbitMQServiceError("Failed to connect to RabbitMQ", e)
        except Exception as e:
            logger.error(f"Unexpected error during RabbitMQService initialization: {e}")
            raise RabbitMQServiceError("Unexpected error during RabbitMQService initialization", e)

    def publish_message(self, message):
        try:
            # Publish the message to the queue
            self.producer.send_message(
                message=message
            )
            logger.info(
                f"Successfully published message to queue {self.queue_name} with exchange key {self.exchange_key}")

        except pika.exceptions.AMQPError as e:
            logger.error(f"Failed to publish message to RabbitMQ: {e}")
            raise RabbitMQServiceError("Failed to publish message to RabbitMQ", e)

        except Exception as e:
            logger.error(f"Unexpected error during message publishing: {e}")
            raise RabbitMQServiceError("Unexpected error during message publishing", e)

    def __del__(self):
        try:
            if self.rabbitmq_connection:
                self.rabbitmq_connection.close_connection()
                logger.info("RabbitMQ connection closed successfully.")
        except Exception as e:
            logger.error(f"Error closing RabbitMQ connection: {e}")
            raise RabbitMQServiceError("Error closing RabbitMQ connection", e)
