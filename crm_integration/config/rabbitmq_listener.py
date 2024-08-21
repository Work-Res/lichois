import pika
import json
import logging

logger = logging.getLogger('rabbitmq_listener')


class RabbitMQListener:

    def __init__(self, connection):
        self.connection = connection
        self.channel = self.connection.connect()

    def callback_work_permit(self, ch, method, properties, body):
        """Process messages from the work_permit_queue."""
        message = json.loads(body)
        logger.info(f"Received message from work_permit_queue: {message}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def callback_citizenship(self, ch, method, properties, body):
        """Process messages from the citizenship_queue."""
        message = json.loads(body)
        logger.info(f"Received message from citizenship_queue: {message}")
        # Process the message (business logic here)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start_listening(self):
        """Start consuming messages from both queues."""
        try:
            # Declare the queues (in case they are not declared elsewhere)
            self.channel.queue_declare(queue='work_permit_queue', durable=True)
            self.channel.queue_declare(queue='citizenship_queue', durable=True)

            # Set up consumers for both queues
            self.channel.basic_consume(queue='work_permit_queue', on_message_callback=self.callback_work_permit)
            self.channel.basic_consume(queue='citizenship_queue', on_message_callback=self.callback_citizenship)

            logger.info("Starting to listen to both queues...")
            self.channel.start_consuming()

        except pika.exceptions.AMQPError as e:
            logger.error(f"Failed to consume messages: {e}")
            raise

    def stop_listening(self):
        """Stop consuming messages and close the connection."""
        if self.channel.is_open:
            self.channel.stop_consuming()
        self.connection.close_connection()
        logger.info("Stopped listening and closed RabbitMQ connection.")
