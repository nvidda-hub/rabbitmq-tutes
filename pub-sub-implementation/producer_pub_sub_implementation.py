import pika
from pika.exchange_type import ExchangeType

connection_params = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

channel.exchange_declare(exchange='pubsub', exchange_type=ExchangeType.fanout)

# in pub sub pattern consumer will have there own queue no need to declare one

message = "Hello this message needs to be broadcasted"

channel.basic_publish(exchange='pubsub', routing_key='', body=message)
print(f"Message send : {message}")

connection.close()