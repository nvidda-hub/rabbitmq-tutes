import pika
from pika.exchange_type import ExchangeType

connection_parameters = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

channel.exchange_declare(exchange='altexchange', exchange_type=ExchangeType.fanout)

channel.exchange_declare(exchange='mainexchange', exchange_type=ExchangeType.direct, arguments={'alternate-exchange': 'altexchange'})

message1 = 'Send this to test queue thorugh Main exchange ==> Hello this is my first message'
message2 = 'Send this to sample queue thorugh Alternate exchange ==> Hello this is my first message'

channel.basic_publish(exchange='mainexchange', routing_key='test', body=message1)        # will go to main exchange because sending to test queue
channel.basic_publish(exchange='mainexchange', routing_key='sample', body=message2)       # will go alt exchange because sending other than test queue

print(f'sent message: {message1}')
print(f'sent message: {message2}')

connection.close()