from mongoengine import Document
from mongoengine import StringField
from mongoengine import IntField

from models import Content


class NavigationOrder(Document):
    route = StringField(unique=True)
    order = IntField(unique=True)

    @staticmethod
    def populate_from_content():
        for i, c in enumerate(Content.get_navigables()):
            NavigationOrder(route=c.route, order=i).save()

    def move(self, order):
        current_order = self.order
        existing_target = NavigationOrder.objects(order=order).first()
        if existing_target is not None:
            existing_target.move(-1)  # Can't guarantee that -1 doesn't have a thing in it, so possible fail here
            self.order = order
            self.save()
            existing_target.move(current_order)
        else:
            self.order = order
            self.save()