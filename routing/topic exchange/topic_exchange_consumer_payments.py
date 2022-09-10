import pika
from pika.exchange_type import ExchangeType


def on_message_received(channel, method, properties, body):
    print(f"Payments service - message received in consumer : {body}")


connection_parameters = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

channel.exchange_declare(exchange='topic_exchange_test', exchange_type=ExchangeType.topic)

queue_name = channel.queue_declare(queue='', exclusive=True)            # exclusive True means when connection closes queue also be deleted

channel.queue_bind(exchange='topic_exchange_test', queue=queue_name.method.queue, routing_key='#.payments') # will match like x.payments or x.v.payments

# in above line hash(#) wildcard matches one or more routing key

channel.basic_consume(queue=queue_name.method.queue, auto_ack=True, on_message_callback=on_message_received)

print("Start consuming")

channel.start_consuming()