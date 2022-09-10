import pika, uuid


class RPCClient:
    def __init__(self) -> None:
        self.connection_params = pika.ConnectionParameters('localhost')
        self.connection = pika.BlockingConnection(self.connection_params)
        self.channel = self.connection.channel()

        queue_name = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue_name = queue_name.method.queue

        self.channel.basic_consume(queue=self.callback_queue_name, 
                                    on_message_callback=self.on_response, 
                                    auto_ack=True)
        self.response = None
        self.correlation_id = None

    def on_response(self, channel, properties, method, body):
        # if self.correlation_id == properties.correlation_id:
        self.response = body
    
    def call(self, n):
        self.response = None
        self.correlation_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='', 
                                    routing_key='rpc_queue', 
                                    properties=pika.BasicProperties(reply_to=self.callback_queue_name, correlation_id=self.correlation_id),
                                    body=str(n))
        self.connection.process_data_events(time_limit=None)
        return int(self.response)

if __name__ == '__main__':
    rpc_client = RPCClient()
    n = int(input("Enter number to calculate fibanacci : "))
    print(f" [x] Requesting fib({n})")
    response = rpc_client.call(n)
    print(f"Got {response}")