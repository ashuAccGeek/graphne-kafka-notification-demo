import graphene
import json
from graphene_django import DjangoObjectType, DjangoListField
from .models import Order,Item
from django.contrib.auth.models import User
from .onesignal_producer import produce_notification_event

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'username')

class ItemType(DjangoObjectType):
    class Meta:
        model = Item
        fields =  ("name" ,"description" ,"price" ,"available")

class OrderType(DjangoObjectType):
    user = graphene.Field(UserType)

    class Meta:
        model = Order
        fields =  ('id', 'user', 'items', 'total_amount', 'delivery_address', 'delivery_time')

class OrderQuery(graphene.ObjectType):
    orders = graphene.List(OrderType)

    def resolve_orders(self, info):
        # Query all Order objects from the database
        return Order.objects.all()


class PlaceOrder(graphene.Mutation):
    class Arguments:
        user = graphene.Int(required=True)
        items = graphene.List(graphene.Int, required=True)
        delivery_address = graphene.String(required=True)
        delivery_time = graphene.DateTime(required=True)

    order = graphene.Field(OrderType)

    @classmethod
    def mutate(cls, root, info, user, items, delivery_address, delivery_time):
        
        # Logic to place an order
        try:
            user = User.objects.get(id=user)
            items = Item.objects.filter(id__in=items)
        except User.DoesNotExist:
            raise Exception("User does not exist")
        except Item.DoesNotExist:
            raise Exception("One or more items do not exist")
        
        # Calculate total amount
        total_amount = sum(item.price for item in items)

        # Create the order
        order = Order.objects.create(
            user=user,
            total_amount=total_amount,
            delivery_address=delivery_address,
            delivery_time=delivery_time
        )
        order.items.set(items)

        # Construct notification event data
        item_names = [item.name for item in items]
        delivery_time_isoformat = delivery_time.isoformat()

        event_data = {
            'username': user.username,
            'items': item_names,
            'delivery_address': delivery_address,
            'delivery_time': delivery_time_isoformat,
        }
        event_data_json = json.dumps(event_data) 

        # Produce notification event to Kafka
        produce_notification_event('kafka_django',event_data_json)

        return PlaceOrder(order=order)

class OrderMutation(graphene.ObjectType):
    place_order = PlaceOrder.Field()


class Query(OrderQuery, graphene.ObjectType):
    pass

class Mutation(OrderMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query,mutation=Mutation)
