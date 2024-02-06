from confluent_kafka import Producer,Consumer
from graphene_django import DjangoObjectType, DjangoListField, DjangoMutation
import graphene
from .models import KafkaEg

# Create your views here.

# Kafka producer configuration
producer_config = {
    'bootstrap.servers': 'localhost:9092',
}

# Kafka consumer configuration
consumer_config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'my-consumer-group',
}

class KafkaEgType(DjangoObjectType):
    class Meta:
        model = KafkaEg
        fields = ('id', 'title')

class KafkaEgQuery(graphene.ObjectType):
    kafka = DjangoListField(KafkaEgType)


class CreateKafkaEg(DjangoMutation):
    class Arguments:
        name = graphene.String(required=True)

    kafka = graphene.Field(KafkaEgType)

    @staticmethod
    def mutate(root, info, title):
        # Produce a message to Kafka topic
        produce_message('kafka_django', f'New KafkaEg created: {title}')

        kafka = KafkaEg.objects.create(title=title)
        return CreateKafkaEg(kafka=kafka)

class KafkaEgMutation(graphene.ObjectType):
    create_kafka = CreateKafkaEg.Field()


# Kafka producer function
def produce_message(topic, message):
    producer = Producer(producer_config)
    producer.produce(topic, message.encode('utf-8'))
    producer.flush()

# Kafka consumer function
def consume_message(topic):
    consumer = Consumer(consumer_config)
    consumer.subscribe([topic])

    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            print("Consumer error: {}".format(msg.error()))
            continue
        print("Received message: {}".format(msg.value().decode('utf-8')))

class Query(KafkaEgQuery, graphene.ObjectType):
    pass

class Mutation(KafkaEgMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)