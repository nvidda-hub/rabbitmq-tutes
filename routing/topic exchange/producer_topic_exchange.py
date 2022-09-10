import pika, random
from pika.exchange_type import ExchangeType


connection_params = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

channel.exchange_declare(exchange='topic_exchange_test', exchange_type=ExchangeType.topic)

user_payment_otp = random.randint(10**6, 10**7)
message1 = f"Your otp for subscription payment{user_payment_otp}. Will be forwarded to user as well as payment consumer"
channel.basic_publish(exchange='topic_exchange_test', routing_key='user.otp.payments', body=message1)

print(f"message sent to analytics : {message1}")

message2 = f"Statiscal data for analysis is {random.randint(10**3, 10**4)}."
channel.basic_publish(exchange='topic_exchange_test', routing_key='user.analytics.new', body=message2)

print(f"message sent for payments : {message2}")


connection.close()