import pika


def on_message_received(channel, method, properties, body):
    print(f"new message received {body}")


connection_params = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

channel.queue_declare(queue='testBox')
channel.basic_consume(queue='testBox', auto_ack=True, on_message_callback=on_message_received)

print("Start consuming.....")

channel.start_consuming()