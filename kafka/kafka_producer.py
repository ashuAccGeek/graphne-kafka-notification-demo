from confluent_kafka import Producer

# Kafka producer configuration
producer_config = {
    'bootstrap.servers': 'localhost:9092',
}

# Kafka producer function
def produce_message(topic, message):
    producer = Producer(producer_config)
    producer.produce(topic, message.encode('utf-8'))
    producer.flush()