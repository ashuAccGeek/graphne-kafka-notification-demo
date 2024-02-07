from graphene_django import DjangoObjectType, DjangoListField
import graphene
from .models import KafkaEg
from .kafka_producer import produce_message
# Create your views here.

#graphQL Queries and Mutations

 #Queries
class KafkaEgType(DjangoObjectType):
    class Meta:
        model = KafkaEg
        fields = ('id', 'title')

class KafkaEgQuery(graphene.ObjectType):
    kafka = DjangoListField(KafkaEgType)


 #Mutation
class CreateKafkaEg(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)

    kafka = graphene.Field(KafkaEgType)

    @classmethod
    def mutate(cls,root, info, title):
        kafka = KafkaEg.objects.create(title=title)

        # Produce a message to Kafka topic
        produce_message('kafka_django', f'New KafkaEg created: {title}')

        return CreateKafkaEg(kafka=kafka)

class KafkaEgMutation(graphene.ObjectType):
    create_kafka = CreateKafkaEg.Field()

class Query(KafkaEgQuery, graphene.ObjectType):
    pass

class Mutation(KafkaEgMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)