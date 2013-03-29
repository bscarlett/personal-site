from mongoengine import Document
from mongoengine import StringField
from mongoengine import IntField


class NavigationOrder(Document):
    route = StringField(unique=True)
    order = IntField(unique=True)

    def move(self, order):
        if self.order == order:
            return
        existing_target = NavigationOrder.objects(order=order).first()
        if existing_target is not None:
            existing_new = {'route': existing_target.route, 'order': self.order}
            existing_target.delete()
            self.order = order
            self.save()
            NavigationOrder(**existing_new).save()
        else:
            self.order = order
            self.save()

    @classmethod
    def add(cls, route):
        nav = cls(route=route, order=cls.highest() + 1)
        nav.save()
        return nav

    @classmethod
    def highest(cls):
        if cls.objects.count() == 0:
            return -1
        return max([o.order for o in cls.objects])

    @classmethod
    def get_routes_in_order(cls):
        return [o.route for o in cls.objects.order_by('order')]
