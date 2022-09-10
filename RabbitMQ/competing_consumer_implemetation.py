import pika, time, random


def on_message_received(channel, method, properties, body):
    processing_time = random.randint(1, 10)
    print(f"new message received {body} and will take {processing_time} to process")
    time.sleep(processing_time)
    channel.basic_ack(delivery_tag=method.delivery_tag)
    print("Done processing the mesaage")


connection_params = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

channel.queue_declare(queue='testCompetingBox')
channel.basic_qos(prefetch_count=1)     # process one message at a time or one consumer will consume one message at a time
channel.basic_consume(queue='testCompetingBox', on_message_callback=on_message_received)

print("Start consuming.....")

channel.start_consuming()