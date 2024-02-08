from confluent_kafka import Consumer

consumer_config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'my-consumer-group',
    'auto.offset.reset': 'earliest'  # Start consuming from the beginning of the topic
}

def consume_message(topic):
    consumer = Consumer(consumer_config)
    consumer.subscribe([topic])

    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                print("Consumer error: {}".format(msg.error()))
                continue
            print("Order placed with the following Details: {}".format(msg.value().decode('utf-8')))
    finally:
        consumer.close()

if __name__ == "__main__":
    topic = 'kafka_django'  
    consume_message(topic)
