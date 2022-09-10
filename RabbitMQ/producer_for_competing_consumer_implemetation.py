import pika, random, time

connection_params = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()
channel.queue_declare(queue='testCompetingBox')

count = 0
while (True):

    otp = random.randint(10**6, 10**7)
    message = f"Message ID : {count} ==> Your otp is {otp}."
    channel.basic_publish(exchange='', routing_key='testCompetingBox', body=message)

    print(f"message sent : {message}")
    time.sleep(random.randint(1, 4))
    count += 1
    if count == 100:
        break