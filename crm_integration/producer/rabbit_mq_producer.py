import pika
import json


import pika
import json


class RabbitMQProducer:
    def __init__(self, connection, queue_name, exchange_key):
        self.queue_name = queue_name
        self.connection = connection
        self.exchange_key = exchange_key
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue_name, durable=True)

    def send_message(self, message, exchange=None, queue_name=None):
        """Send a message to the default queue or a specified queue."""
        if queue_name:
            self.channel.queue_declare(queue=queue_name, durable=True)
        else:
            queue_name = self.queue_name

        self.channel.basic_publish(
            exchange=self.exchange or exchange,
            routing_key=self.queue_name or queue_name,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            ))
        print(f" [x] Sent {message} to {queue_name}")

    def send_message_to_specific_queue(self, message, queue_name=None, exchange=None):
        """Send a message to a specified queue."""
        self.channel.queue_declare(queue=queue_name, durable=True)
        self.channel.basic_publish(
            exchange=self.exchange or exchange,
            routing_key=self.queue_name or queue_name,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            ))
        print(f" [x] Sent {message} to {queue_name}")

    def close_connection(self):
        self.connection.close()
