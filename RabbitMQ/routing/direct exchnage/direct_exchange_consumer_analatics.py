import pika
from pika.exchange_type import ExchangeType


def on_message_received(channel, method, properties, body):
    print(f"Analytics service - message received in consumer : {body}")


connection_parameters = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

channel.exchange_declare(exchange='routing', exchange_type=ExchangeType.direct)

queue_name = channel.queue_declare(queue='', exclusive=True)            # exclusive True means when connection closes queue also be deleted

channel.queue_bind(exchange='routing', queue=queue_name.method.queue, routing_key='analytics')
channel.queue_bind(exchange='routing', queue=queue_name.method.queue, routing_key='both')

channel.basic_consume(queue=queue_name.method.queue, auto_ack=True, on_message_callback=on_message_received)

print("Start consuming")

channel.start_consuming()