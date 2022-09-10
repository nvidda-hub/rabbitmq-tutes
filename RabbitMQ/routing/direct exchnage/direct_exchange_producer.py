import pika, random
from pika.exchange_type import ExchangeType


connection_params = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

channel.exchange_declare(exchange='routing', exchange_type=ExchangeType.direct)

otp = random.randint(10**6, 10**7)
message1 = f"Statics of analytical data {otp}."
channel.basic_publish(exchange='routing', routing_key='analytics', body=message1)

print(f"message sent to analytics : {message1}")

message2 = f"Your payment otp is {otp}."
channel.basic_publish(exchange='routing', routing_key='payments', body=message2)

print(f"message sent for payments : {message2}")

message3 = f"this is common message."
channel.basic_publish(exchange='routing', routing_key='both', body=message3)

connection.close()