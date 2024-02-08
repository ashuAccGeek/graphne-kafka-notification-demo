from confluent_kafka import Consumer
from onsignalNotifications import send_notification_onsignal,send_sms_notification

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

            # Extract necessary information from the Kafka message
            message_data = msg.value().decode('utf-8')

            # Construct notification payload
            # notification_body = {
            #     'contents': {'en': message_data},
            #     'included_segments': ['Active Users'],
            # }

            # notification_payload = {
            #     'contents': {'en': message_data},
            # }
            # Send push notification using OneSignal
            ## send_notification_onsignal(notification_body)
            send_sms_notification(message_data)
    finally:
        consumer.close()

if __name__ == "__main__":
    topic = 'kafka_django'  
    consume_message(topic)
