import pika
import logging

logger = logging.getLogger('rabbitmq_setup')


class RabbitMQConnection:
    def __init__(self, host='localhost', username='guest', password='guest', vhost='/'):
        self.host = host
        self.credentials = pika.PlainCredentials(username, password)
        self.vhost = vhost
        self.connection = None
        self.channel = None

    def connect(self):
        """Establish a connection to RabbitMQ with the specified vhost."""
        try:
            connection_params = pika.ConnectionParameters(
                host=self.host,
                virtual_host=self.vhost,
                credentials=self.credentials
            )
            self.connection = pika.BlockingConnection(connection_params)
            self.channel = self.connection.channel()
            logger.info(f"Connected to RabbitMQ at {self.host} on vhost '{self.vhost}' "
                        f"with user '{self.credentials.username}'")
            return self.channel
        except pika.exceptions.AMQPConnectionError as e:
            logger.error(f"Failed to connect to RabbitMQ at {self.host} on "
                         f"vhost '{self.vhost}' with user '{self.credentials.username}': {e}")
            raise

    def close_connection(self):
        """Close the connection to RabbitMQ."""
        if self.connection:
            try:
                self.connection.close()
                logger.info("Connection to RabbitMQ closed.")
            except pika.exceptions.AMQPError as e:
                logger.error(f"Failed to close RabbitMQ connection: {e}")
