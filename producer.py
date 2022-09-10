import pika, random

connection_params = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()
channel.queue_declare(queue='testBox')

otp = random.randint(10**6, 10**7)
message = f"Your otp is {otp}."
channel.basic_publish(exchange='', routing_key='testBox', body=message)

print(f"message sent : {message}")

connection.close()