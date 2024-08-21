import pika
import logging

logger = logging.getLogger('rabbitmq_setup')


class RabbitMQConfig:

    def __init__(self, connection):
        self.connection = connection
        self.channel = self.connection.connect()

    def create_exchange(self, exchange_name, exchange_type='direct', durable=True):
        """Create an exchange with the given parameters."""
        try:
            self.channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type, durable=durable)
            logger.info(f"Exchange '{exchange_name}' created or already exists.")
        except pika.exceptions.AMQPError as e:
            logger.error(f"Failed to create exchange '{exchange_name}': {e}")
            raise

    def create_queue(self, queue_name, durable=True):
        """Create a queue with the given parameters."""
        try:
            self.channel.queue_declare(queue=queue_name, durable=durable)
            logger.info(f"Queue '{queue_name}' created or already exists.")
        except pika.exceptions.AMQPError as e:
            logger.error(f"Failed to create queue '{queue_name}': {e}")
            raise

    def bind_queue_to_exchange(self, queue_name, exchange_name, routing_key=''):
        """Bind a queue to an exchange with a specific routing key."""
        try:
            self.channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=routing_key)
            logger.info(f"Queue '{queue_name}' bound to exchange '{exchange_name}' with routing key '{routing_key}'.")
        except pika.exceptions.AMQPError as e:
            logger.error(f"Failed to bind queue '{queue_name}' to exchange '{exchange_name}': {e}")
            raise

    def setup(self):
        """Set up RabbitMQ exchanges, queues, and their bindings."""
        try:
            # Define exchanges, queues, and bindings
            exchanges = [
                {'name': 'work_permit_exchange', 'type': 'direct', 'durable': True},
                {'name': 'citizenship_exchange', 'type': 'direct', 'durable': True},
            ]

            queues = [
                {'name': 'work_permit_queue', 'durable': True, 'exchange': 'work_permit_exchange',
                 'routing_key': 'work_permit'},
                {'name': 'citizenship_queue', 'durable': True, 'exchange': 'citizenship_exchange',
                 'routing_key': 'citizenship'}
            ]

            # Create exchanges
            for exchange in exchanges:
                self.create_exchange(exchange['name'], exchange_type=exchange['type'], durable=exchange['durable'])

            # Create queues and bind them to exchanges
            for queue in queues:
                self.create_queue(queue['name'], durable=queue['durable'])
                self.bind_queue_to_exchange(queue['name'], queue['exchange'], routing_key=queue['routing_key'])

            logger.info("RabbitMQ setup complete.")
        except Exception as e:
            logger.error(f"RabbitMQ setup failed: {e}")
        finally:
            self.connection.close_connection()
