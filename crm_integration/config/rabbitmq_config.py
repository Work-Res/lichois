import pika
import logging

logger = logging.getLogger('rabbitmq_setup')


class RabbitMQConfig:
    def __init__(self, host='localhost', username='guest', password='guest', vhost='/'):
        self.host = host
        self.credentials = pika.PlainCredentials(username, password)  # Set up credentials
        self.vhost = vhost
        self.connection = None
        self.channel = None

    def connect(self):
        """Establish a connection to RabbitMQ with vhost."""
        try:
            connection_params = pika.ConnectionParameters(
                host=self.host,
                virtual_host=self.vhost,  # Specify the vhost
                credentials=self.credentials
            )
            self.connection = pika.BlockingConnection(connection_params)
            self.channel = self.connection.channel()
            logger.info(f"Connected to RabbitMQ at {self.host} on vhost '{self.vhost}' with user '{self.credentials.username}'")
        except pika.exceptions.AMQPConnectionError as e:
            logger.error(f"Failed to connect to RabbitMQ at {self.host} on vhost '{self.vhost}' with user '{self.credentials.username}': {e}")
            raise

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
            self.connect()

            # Define exchanges, queues, and bindings
            exchanges = [
                {'name': 'work_permit_exchange', 'type': 'direct', 'durable': True},
                {'name': 'citizenship_exchange', 'type': 'direct', 'durable': True},
            ]

            queues = [
                {'name': 'work_permit_queue', 'durable': True, 'exchange': 'work_permit_exchange', 'routing_key': 'work_permit'},
                {'name': 'citizenship_queue', 'durable': True, 'exchange': 'citizenship_exchange', 'routing_key': 'citizenship'}
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
            self.close_connection()

    def close_connection(self):
        """Close the connection to RabbitMQ."""
        if self.connection:
            try:
                self.connection.close()
                logger.info("Connection to RabbitMQ closed.")
            except pika.exceptions.AMQPError as e:
                logger.error(f"Failed to close RabbitMQ connection: {e}")
